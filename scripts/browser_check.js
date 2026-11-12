#!/usr/bin/env node
// Dev tool: open a generated HTML page in a real browser and check its behaviour.
// Needs Playwright (`npm i -D playwright` or a global install) with a Chromium browser.
//
//   node scripts/browser_check.js <page.html> [--deck] [--offline] [--graph]
//
// Default checks: diagrams render, no console errors, zoom, section collapse (aria-expanded),
// theme toggle re-renders diagrams, section filter, print layout. --deck: presentation mode (pages with
// .cm-slide sections). --offline: block the CDN and expect the diagram fallback. --graph: the relation-map
// graph (pages with ul.cm-graph): drawing, folding, hover/pin focus, full screen.
// Exit code 1 if any check fails; the last line is a JSON summary.
const { chromium } = require('playwright');
const path = require('path');

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith('--'));
const deck = args.includes('--deck');
const offline = args.includes('--offline');
const graph = args.includes('--graph');
if (!file) { console.error('usage: browser_check.js <page.html> [--deck] [--offline] [--graph]'); process.exit(2); }

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1360, height: 900 } });
  if (offline) await ctx.route('**/cdn.jsdelivr.net/**', (r) => r.abort());
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push('pageerror: ' + e));
  if (!offline) page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  await page.goto('file://' + path.resolve(file));

  const result = {};
  const failures = [];
  const expect = (cond, msg) => { if (!cond) failures.push(msg); };

  if (offline) {
    await page.waitForTimeout(2500);
    result.figures = await page.locator('figure.cm-diagram').count();
    result.offlineFigures = await page.locator('figure.cm-diagram.offline').count();
    result.svgs = await page.locator('pre.mermaid svg').count();
    expect(result.figures === result.offlineFigures, 'every diagram falls back when the CDN is blocked');
    expect(result.svgs === 0, 'no diagram is drawn offline');
    expect(await page.locator('#cm-toc a').count() > 0, 'contents still built offline');
  } else {
    const hasDiagram = (await page.locator('pre.mermaid').count()) > 0;
    if (hasDiagram) await page.waitForSelector('pre.mermaid svg', { timeout: 20000 });
    result.svgs = await page.locator('pre.mermaid svg').count();
    if (hasDiagram) {
      const before = await page.locator('pre.mermaid').first().evaluate((e) => e.style.width || '100%');
      await page.locator('.cm-toolbar button').nth(1).click();
      const after = await page.locator('pre.mermaid').first().evaluate((e) => e.style.width || '100%');
      expect(before !== after, 'zoom changes the diagram width');
    }
    await page.locator('.cm-section > h2 button').first().click();
    result.ariaAfterCollapse = await page.locator('.cm-section > h2 button').first().getAttribute('aria-expanded');
    expect(result.ariaAfterCollapse === 'false', 'collapse sets aria-expanded=false');
    await page.click('#cm-theme');
    await page.waitForTimeout(1500);
    result.theme = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
    expect(result.theme === 'dark', 'theme toggle switches to dark');
    if (hasDiagram) expect((await page.locator('pre.mermaid svg').count()) === result.svgs, 'diagrams are re-rendered after the theme change');
    await page.fill('#cm-search', 'zzzz-no-match');
    const total = await page.locator('.cm-section').count();
    expect((await page.locator('.cm-section[hidden]').count()) === total, 'filter hides every section when nothing matches');
    await page.fill('#cm-search', '');
    // structure tree: collapse all / expand all
    if ((await page.locator('ul.cm-tree').count()) > 0) {
      await page.evaluate(() => document.querySelectorAll('.cm-section.collapsed').forEach((sec) => sec.classList.remove('collapsed')));
      const total = await page.locator('ul.cm-tree details').count();
      await page.getByRole('button', { name: /모두 접기|Collapse all/ }).first().click();
      const closed = await page.locator('ul.cm-tree details:not([open])').count();
      await page.getByRole('button', { name: /모두 펼치기|Expand all/ }).first().click();
      const opened = await page.locator('ul.cm-tree details[open]').count();
      result.tree = { nodes: total, closedAfterCollapse: closed, openAfterExpand: opened };
      expect(total > 0 && closed === total, 'tree: collapse all closes every node');
      expect(opened === total, 'tree: expand all opens every node');
    }
    // print layout: no diagram may be wider than the page, and the legend must stay visible
    await page.emulateMedia({ media: 'print' });
    await page.setViewportSize({ width: 700, height: 900 }); // about the printable width of A4
    const overflow = await page.evaluate(() => {
      const limit = document.documentElement.clientWidth + 1;
      return Array.from(document.querySelectorAll('pre.mermaid svg')).filter((svg) => svg.getBoundingClientRect().right > limit).length;
    });
    expect(overflow === 0, 'print: ' + overflow + ' diagram(s) run past the page width');
    const legendUsed = await page.evaluate(() => !document.getElementById('cm-legend').hidden);
    if (legendUsed) expect(await page.locator('#cm-legend').isVisible(), 'print: the legend stays visible');
    await page.setViewportSize({ width: 1360, height: 900 });
    await page.emulateMedia({ media: 'screen' });
    expect(await page.evaluate(() => /^\d{4}-\d{2}-\d{2}/.test(document.querySelector('.cm-stats dd').textContent)), 'header shows the generated date');
  }

  if (graph) try {
    page.setDefaultTimeout(8000);
    await page.evaluate(() => document.querySelectorAll('.cm-section.collapsed').forEach((sec) => sec.classList.remove('collapsed')));
    const info = await page.evaluate(() => {
      const lis = Array.from(document.querySelectorAll('ul.cm-graph > li'));
      const edges = [];
      lis.forEach((li) => li.querySelectorAll(':scope > ul > li[data-to]').forEach((e) => edges.push([li.id, e.getAttribute('data-to')])));
      return { nodes: lis.length, ids: lis.map((li) => li.id), edges, groups: Array.from(new Set(lis.map((li) => li.getAttribute('data-group')))) };
    });
    const uniqueEdges = new Set(info.edges.map((e) => e.join('>'))).size;
    result.graph = { nodes: info.nodes, edges: uniqueEdges };
    if (uniqueEdges === 0) {
      expect((await page.locator('.cm-graph-empty').count()) === 1, 'graph: a graph without edges shows the empty-state note');
      expect((await page.locator('svg.cm-graph-svg').count()) === 0, 'graph: nothing is drawn when there are no edges');
      expect(await page.locator('ul.cm-graph').isVisible(), 'graph: the plain list stays visible when there is nothing to draw');
    } else {
      await page.waitForSelector('svg.cm-graph-svg', { timeout: 10000 }).catch(() => {});
      expect((await page.locator('svg.cm-graph-svg').count()) === 1, 'graph: one svg for the list');
      expect((await page.locator('g.cm-node').count()) === info.nodes, 'graph: one g.cm-node per list item');
      expect(!(await page.locator('ul.cm-graph').isVisible()), 'graph: the plain list is hidden on screen');
      const edgeCheck = await page.evaluate((ids) => {
        const known = new Set(ids);
        const ps = Array.from(document.querySelectorAll('path.cm-edge:not(.cm-agg)'));
        return { count: ps.length, dangling: ps.filter((q) => !known.has(q.getAttribute('data-from')) || !known.has(q.getAttribute('data-to'))).length };
      }, info.ids);
      expect(edgeCheck.count === uniqueEdges, 'graph: one path.cm-edge per edge (' + edgeCheck.count + ' vs ' + uniqueEdges + ')');
      expect(edgeCheck.dangling === 0, 'graph: every edge joins two known nodes');
      const groups = await page.$$eval('g.cm-group', (gs) => gs.map((g) => g.getAttribute('data-group')).sort());
      expect(JSON.stringify(groups) === JSON.stringify(info.groups.slice().sort()), 'graph: groups are keyed by the full folder path');
      const folded = info.nodes >= 80;
      const collapsedGroups = await page.locator('g.cm-group.collapsed').count();
      const visibleNodes = () => page.evaluate(() => Array.from(document.querySelectorAll('g.cm-node')).filter((n) => n.getBoundingClientRect().width > 0).length);
      if (folded) {
        expect(collapsedGroups === groups.length, 'graph: 80+ files start with every folder box folded');
        expect((await page.locator('path.cm-edge.cm-agg').count()) > 0, 'graph: folded boxes are joined by aggregate edges');
        expect((await visibleNodes()) === 0, 'graph: no file node shows while folded');
        await page.locator('g.cm-group.collapsed rect.cm-group-box').first().click();
        expect((await page.locator('g.cm-group.collapsed').count()) === groups.length - 1, 'graph: clicking a folded box expands it');
        expect((await visibleNodes()) > 0, 'graph: the expanded box shows its files');
      } else {
        expect(collapsedGroups === 0, 'graph: fewer than 80 files start expanded');
        expect((await visibleNodes()) === info.nodes, 'graph: every file node shows');
        const overlaps = await page.evaluate(() => {
          const r = Array.from(document.querySelectorAll('g.cm-node')).map((n) => n.getBoundingClientRect());
          let bad = 0;
          for (let i = 0; i < r.length; i++) for (let j = i + 1; j < r.length; j++) {
            const w = Math.min(r[i].right, r[j].right) - Math.max(r[i].left, r[j].left);
            const h = Math.min(r[i].bottom, r[j].bottom) - Math.max(r[i].top, r[j].top);
            if (w > 1 && h > 1) bad++;
          }
          return bad;
        });
        expect(overlaps === 0, 'graph: ' + overlaps + ' overlapping node pair(s)');
      }

      // ---- focus: hover, pin, keyboard, side panel (direct neighbours only) ----
      const rel = await page.evaluate(() => {
        const m = {};
        const lis = Array.from(document.querySelectorAll('ul.cm-graph > li'));
        lis.forEach((li) => { m[li.id] = { uses: [], usedBy: [], path: li.querySelector('code').textContent }; });
        lis.forEach((li) => li.querySelectorAll(':scope > ul > li[data-to]').forEach((e) => { m[li.id].uses.push(e.getAttribute('data-to')); m[e.getAttribute('data-to')].usedBy.push(li.id); }));
        return m;
      });
      const ids = Object.keys(rel);
      const away = () => page.mouse.move(2, 2);
      const states = () => page.locator('.is-focus, .is-uses, .is-usedby, .is-dim, .is-hot').count();
      const ids_of = (sel) => page.$$eval(sel, (els) => els.map((e) => e.getAttribute('data-id')).sort());
      if (!folded) {
        const degree = (i) => rel[i].uses.length + rel[i].usedBy.length;
        const hub = ids.slice().sort((a, c) => degree(c) - degree(a))[0], h = rel[hub]; // the busiest file (g1 may have no edges)
        await page.locator('g.cm-node[data-id="' + hub + '"]').hover();
        expect(JSON.stringify(await ids_of('g.cm-node.is-uses')) === JSON.stringify(h.uses.slice().sort()), 'focus: hover marks exactly the files the hovered file uses');
        expect(JSON.stringify(await ids_of('g.cm-node.is-usedby')) === JSON.stringify(h.usedBy.slice().sort()), 'focus: hover marks exactly the files that use the hovered file');
        expect((await ids_of('g.cm-node.is-focus')).join() === hub, 'focus: the hovered file is marked is-focus');
        const near = new Set([hub, ...h.uses, ...h.usedBy]);
        const others = ids.filter((i) => !near.has(i));
        expect(JSON.stringify(await ids_of('g.cm-node.is-dim')) === JSON.stringify(others.sort()), 'focus: every non-neighbour (including 2-step ones) is dimmed');
        expect((await page.locator('path.cm-edge.is-hot:not(.cm-agg)').count()) === h.uses.length + h.usedBy.length, 'focus: only edges touching the hovered file are hot');
        if (rel.g2 && rel.g3 && rel.g2.uses.includes('g3') && rel.g3.uses.includes('g2')) {
          await page.locator('g.cm-node[data-id="g2"]').hover();
          expect(await page.locator('g.cm-node[data-id="g3"]').evaluate((e) => e.classList.contains('is-uses') && e.classList.contains('is-usedby')), 'focus: a mutual import is marked both ways');
        }
        await away();
        expect((await states()) === 0, 'focus: moving the mouse away clears every state class');
        // click pins, click again unpins
        await page.locator('g.cm-node[data-id="' + hub + '"]').click();
        await away();
        expect((await page.locator('figure.cm-graph-view').getAttribute('data-pinned')) === hub, 'pin: clicking pins the file');
        expect((await ids_of('g.cm-node.is-focus')).join() === hub, 'pin: the highlight stays after the mouse leaves');
        const panelText = await page.locator('.cm-graph-panel').innerText();
        expect(panelText.includes(h.path), 'panel: shows the pinned file path');
        expect((await page.locator('.cm-graph-panel button.cm-gp-link').count()) === h.uses.length + h.usedBy.length, 'panel: lists every neighbour as a button');
        const firstLink = page.locator('.cm-graph-panel button.cm-gp-link').first();
        const target = await firstLink.getAttribute('data-id');
        await firstLink.click();
        expect((await page.locator('figure.cm-graph-view').getAttribute('data-pinned')) === target, 'panel: a neighbour button moves the pin to that file');
        await page.keyboard.press('Escape');
        expect((await page.locator('figure.cm-graph-view').getAttribute('data-pinned')) === null, 'pin: Escape unpins');
        expect((await page.locator('.cm-graph-panel').innerText()).trim() === '', 'panel: empty when nothing is pinned');
        await page.locator('g.cm-node[data-id="' + hub + '"]').click();
        await page.locator('g.cm-node[data-id="' + hub + '"]').click();
        await away();
        expect((await page.locator('figure.cm-graph-view').getAttribute('data-pinned')) === null, 'pin: clicking the pinned file again unpins');
        expect((await states()) === 0, 'pin: no state class is left after unpinning and leaving');
        // keyboard: focus highlights, Enter pins, Escape unpins
        await page.evaluate(() => document.activeElement && document.activeElement.blur()); // a click leaves the node focused
        await page.locator('g.cm-node[data-id="' + hub + '"]').focus();
        expect((await ids_of('g.cm-node.is-focus')).join() === hub, 'keyboard: focusing a node highlights it');
        await page.keyboard.press('Enter');
        expect((await page.locator('figure.cm-graph-view').getAttribute('data-pinned')) === hub, 'keyboard: Enter pins the focused node');
        await page.keyboard.press('Escape');
        await page.evaluate(() => document.activeElement && document.activeElement.blur());
        expect((await states()) === 0, 'keyboard: nothing is left highlighted after Escape and blur');
      } else {
        // folded graph: hovering a folded box marks the boxes it is linked to
        const aggs = await page.$$eval('path.cm-agg', (ps) => ps.map((q) => [q.getAttribute('data-from-group'), q.getAttribute('data-to-group')]));
        const key = await page.locator('g.cm-group.collapsed').first().getAttribute('data-group');
        await page.locator('g.cm-group[data-group="' + key + '"] rect.cm-group-box').hover();
        const linked = new Set(); let touching = 0;
        aggs.forEach(([a, b]) => { if (a === key || b === key) { linked.add(a); linked.add(b); touching++; } });
        linked.delete(key);
        const dimmedGroups = await page.locator('g.cm-group.is-dim').count();
        expect(dimmedGroups === groups.length - 1 - linked.size, 'focus: hovering a folded box dims the boxes it is not linked to (' + dimmedGroups + ' vs ' + (groups.length - 1 - linked.size) + ')');
        expect((await page.locator('path.cm-agg.is-hot').count()) === touching, 'focus: only aggregate edges touching the hovered box are hot');
        await away();
        expect((await states()) === 0, 'focus: leaving a folded box clears every state class');
        if (info.nodes >= 500) {
          // a hub with many neighbours must react quickly
          const gk = rel.g1 ? await page.locator('g.cm-node[data-id="g1"]').getAttribute('data-group') : null;
          if (await page.locator('g.cm-group.collapsed[data-group="' + gk + '"]').count()) await page.locator('g.cm-group[data-group="' + gk + '"] rect.cm-group-box').click();
          const ms = await page.evaluate(() => {
            const el = document.querySelector('g.cm-node[data-id="g1"]');
            const t0 = performance.now(); el.dispatchEvent(new MouseEvent('mouseover', { bubbles: true })); return performance.now() - t0;
          });
          result.hubHoverMs = Math.round(ms);
          expect(rel.g1.usedBy.length >= 100, 'focus: the 600-file fixture has a hub with 100+ users');
          expect(ms < 100, 'focus: hovering a hub took ' + Math.round(ms) + ' ms (limit 100)');
        }
      }

      // ---- view: zoom, fit, pan, full screen, theme, print, speed ----
      const stageBox = () => page.locator('svg.cm-graph-svg').evaluate((e) => { const r = e.getBoundingClientRect(); return { w: r.width, h: r.height }; });
      const b0 = await stageBox();
      const vb = await page.locator('svg.cm-graph-svg').getAttribute('viewBox');
      const [, , vw, vh] = vb.split(' ').map(Number);
      expect(Math.abs(b0.h / b0.w - vh / vw) < 0.01, 'view: the svg keeps its aspect ratio (no blank band when it is scaled down)');
      await page.locator('.cm-graph-zoom-in').click();
      const b1 = await stageBox();
      expect(b1.w > b0.w * 1.1, 'view: zoom in widens the graph');
      await page.locator('.cm-graph-zoom-out').click(); await page.locator('.cm-graph-zoom-out').click();
      expect((await stageBox()).w < b1.w, 'view: zoom out narrows the graph');
      await page.locator('.cm-graph-fit').click();
      expect(Math.abs((await stageBox()).w - b0.w) < 2, 'view: fit restores the initial width');
      // pan by dragging an empty spot (and the drag must not click anything)
      for (let i = 0; i < 4; i++) await page.locator('.cm-graph-zoom-in').click();
      await page.evaluate(() => { const st = document.querySelector('.cm-graph-stage'); st.scrollLeft = 200; st.scrollTop = 100; });
      const spot = await page.evaluate(() => {
        const st = document.querySelector('.cm-graph-stage'), r = st.getBoundingClientRect();
        for (let y = r.top + 8; y < r.bottom - 24; y += 16) for (let x = r.left + 8; x < r.right - 24; x += 16) {
          const el = document.elementFromPoint(x, y);
          if (el && st.contains(el) && !el.closest('.cm-node, .cm-group-toggle, .cm-graph-panel, .cm-graph-tools')) return { x, y };
        }
        return null;
      });
      expect(spot !== null, 'view: the zoomed graph has an empty spot to drag from');
      if (spot) {
        const read = () => page.evaluate(() => { const st = document.querySelector('.cm-graph-stage'); return { l: st.scrollLeft, t: st.scrollTop, ml: st.scrollWidth - st.clientWidth, mt: st.scrollHeight - st.clientHeight }; });
        const before = await read();
        await page.mouse.move(spot.x, spot.y); await page.mouse.down(); await page.mouse.move(spot.x + 40, spot.y + 30, { steps: 4 }); await page.mouse.up();
        const after = await read();
        // only an axis that really overflows can scroll (a small graph may not overflow vertically)
        if (before.ml > 1 || before.mt > 1) expect((before.ml <= 1 || after.l < before.l) && (before.mt <= 1 || after.t < before.t) && (after.l < before.l || after.t < before.t), 'view: dragging an empty spot pans the graph');
      }
      await page.locator('.cm-graph-fit').click();
      // full screen: native API first, fixed overlay as the fallback; Escape leaves it before it unpins
      const fits = () => page.locator('figure.cm-graph-view').evaluate((e) => { const r = e.getBoundingClientRect(); return Math.abs(r.width - innerWidth) < 2 && Math.abs(r.height - innerHeight) < 2; });
      await page.locator('.cm-graph-fs').click();
      expect(await page.locator('figure.cm-graph-view.cm-graph-full').count() === 1, 'full screen: the figure gets cm-graph-full');
      expect(await fits(), 'full screen: the graph fills the viewport');
      const someNode = (await page.$$eval('g.cm-node:not(.cm-off)', (n) => n.length)) > 0 ? await page.$$eval('g.cm-node:not(.cm-off)', (n) => n[0].getAttribute('data-id')) : null;
      if (someNode) {
        await page.locator('g.cm-node[data-id="' + someNode + '"]').click();
        await page.keyboard.press('Escape');
        expect(await page.locator('figure.cm-graph-view.cm-graph-full').count() === 0, 'full screen: the first Escape leaves full screen');
        expect((await page.locator('figure.cm-graph-view').getAttribute('data-pinned')) === someNode, 'full screen: leaving it keeps the pin');
        await page.keyboard.press('Escape');
        expect((await page.locator('figure.cm-graph-view').getAttribute('data-pinned')) === null, 'full screen: the second Escape unpins');
      }
      await page.evaluate(() => { Element.prototype.requestFullscreen = () => Promise.reject(new Error('blocked')); });
      await page.locator('.cm-graph-fs').click();
      await page.waitForTimeout(150);
      expect(await page.locator('figure.cm-graph-view.cm-graph-full').count() === 1 && await fits(), 'full screen: still works when the browser blocks the Fullscreen API');
      await page.locator('.cm-graph-fs').click();
      expect(await page.locator('figure.cm-graph-view.cm-graph-full').count() === 0, 'full screen: the button leaves it too');
      // theme: node colours follow the page theme in both directions
      const lum = (c) => { const m = c.match(/\d+(\.\d+)?/g).map(Number); return (0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]) / 255; };
      const colours = () => page.evaluate(() => {
        const n = document.querySelector('g.cm-node[data-kind="source"]');
        return { fill: getComputedStyle(n.querySelector('rect')).fill, text: getComputedStyle(n.querySelector('text')).fill };
      });
      const c1 = await colours();
      await page.click('#cm-theme'); await page.waitForTimeout(300);
      const c2 = await colours();
      expect(Math.abs(lum(c1.fill) - lum(c2.fill)) > 0.4, 'theme: the node fill changes with the theme');
      expect(Math.abs(lum(c1.fill) - lum(c1.text)) > 0.4 && Math.abs(lum(c2.fill) - lum(c2.text)) > 0.4, 'theme: node labels stay readable in both themes');
      // print: the page shows the plain list instead of the figure
      await page.emulateMedia({ media: 'print' });
      await page.setViewportSize({ width: 700, height: 900 });
      expect(!(await page.locator('figure.cm-graph-view').isVisible()) && (await page.locator('ul.cm-graph').isVisible()), 'print: the list replaces the figure');
      await page.setViewportSize({ width: 1360, height: 900 });
      await page.emulateMedia({ media: 'screen' });
      // speed
      const buildMs = Number(await page.locator('figure.cm-graph-view').getAttribute('data-build-ms'));
      result.graphBuildMs = buildMs;
      expect(Number.isFinite(buildMs), 'speed: the figure records data-build-ms');
      if (info.nodes >= 500) expect(buildMs < 3000, 'speed: first layout of ' + info.nodes + ' files took ' + buildMs + ' ms (limit 3000)');

      // ---- review fixes ----
      // edges must not run through a file (or folder box) they do not belong to: the resting picture may not show relations that do not exist
      const crossings = await page.evaluate(() => {
        const rects = (sel) => Array.from(document.querySelectorAll(sel)).filter((g) => g.getBoundingClientRect().width > 0).map((g) => {
          const r = g.querySelector('rect'); return { id: g.getAttribute('data-id') || g.getAttribute('data-group'), x: +r.getAttribute('x'), y: +r.getAttribute('y'), w: +r.getAttribute('width'), h: +r.getAttribute('height') };
        });
        const nodes = rects('g.cm-node'), boxes = rects('g.cm-group');
        let bad = 0, sample = null;
        const walk = (p, own, others) => {
          const L = p.getTotalLength();
          for (let i = 1; i < 60; i++) {
            const pt = p.getPointAtLength(L * i / 60);
            for (const n of others) {
              if (own.includes(n.id)) continue;
              if (pt.x > n.x + 1 && pt.x < n.x + n.w - 1 && pt.y > n.y + 1 && pt.y < n.y + n.h - 1) { bad++; if (!sample) sample = own.join('>') + ' through ' + n.id; return; }
            }
          }
        };
        document.querySelectorAll('path.cm-edge:not(.cm-agg):not(.cm-off)').forEach((p) => walk(p, [p.getAttribute('data-from'), p.getAttribute('data-to')], nodes));
        document.querySelectorAll('path.cm-agg:not(.cm-off)').forEach((p) => walk(p, [p.getAttribute('data-from-group'), p.getAttribute('data-to-group')], boxes));
        return { bad, sample };
      });
      expect(crossings.bad === 0, 'edges: ' + crossings.bad + ' edge(s) run through a file or folder box they do not belong to (' + crossings.sample + ')');

      // the pinned panel sits beside the stage (below it on a narrow screen), never over it
      const pinTarget = await page.evaluate(() => { const n = Array.from(document.querySelectorAll('g.cm-node')).find((g) => g.getBoundingClientRect().width > 0); return n ? n.getAttribute('data-id') : null; });
      if (pinTarget) {
        const overlap = (a, b) => Math.min(a.right, b.right) - Math.max(a.left, b.left) > 1 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 1;
        const rectOf = (sel) => page.locator(sel).evaluate((e) => { const r = e.getBoundingClientRect(); return { left: r.left, right: r.right, top: r.top, bottom: r.bottom }; });
        await page.locator('g.cm-node[data-id="' + pinTarget + '"]').click();
        expect(!overlap(await rectOf('.cm-graph-panel'), await rectOf('.cm-graph-stage')), 'panel: on a wide screen the panel does not cover the graph');
        await page.setViewportSize({ width: 390, height: 800 });
        await page.waitForTimeout(150);
        const narrowPanel = await rectOf('.cm-graph-panel'), narrowStage = await rectOf('.cm-graph-stage');
        expect(!overlap(narrowPanel, narrowStage) && narrowPanel.top >= narrowStage.bottom - 1, 'panel: on a narrow screen the panel sits below the graph');
        await page.locator('.cm-graph-fit').click();
        const fitRatio = await page.locator('svg.cm-graph-svg').evaluate((e) => e.getBoundingClientRect().width / e.viewBox.baseVal.width);
        expect(fitRatio >= 0.69, 'view: a phone-width fit stays at or above 70% (' + fitRatio.toFixed(2) + ')');
        await page.setViewportSize({ width: 1360, height: 900 });
        await page.keyboard.press('Escape');
        // keyboard focus is not lost: unpinning returns it to the node, and a panel link moves it to the new node
        await page.locator('g.cm-node[data-id="' + pinTarget + '"]').click();
        const link = page.locator('.cm-graph-panel button.cm-gp-link').first();
        if (await link.count()) {
          const next = await link.getAttribute('data-id');
          await link.click();
          expect((await page.evaluate(() => document.activeElement && document.activeElement.getAttribute('data-id'))) === next, 'focus: a panel link moves focus to the newly pinned node');
          expect((await page.locator('g.cm-node[data-id="' + next + '"]').getAttribute('aria-pressed')) === 'true', 'a11y: the pinned node has aria-pressed=true');
        }
        await page.keyboard.press('Escape');
        expect((await page.evaluate(() => document.activeElement && document.activeElement.classList.contains('cm-node'))), 'focus: Escape leaves focus on a node, not on the page body');
        await page.evaluate(() => document.activeElement && document.activeElement.blur());
        await away();
      }
      expect((await page.locator('.cm-graph-stage').getAttribute('tabindex')) === '0' && (await page.locator('.cm-graph-stage').getAttribute('role')) === 'region', 'a11y: the scrollable stage is keyboard reachable and labelled');
      expect((await page.locator('.cm-graph-panel').getAttribute('aria-live')) === 'polite', 'a11y: the panel announces changes');
      // the key explains every node style that is on the page
      const kinds = await page.$$eval('g.cm-node', (n) => Array.from(new Set(n.map((x) => x.getAttribute('data-kind')))));
      const keyItems = await page.locator('.cm-graph-key span').count();
      expect(keyItems === 2 + kinds.filter((k) => k !== 'source').length, 'key: one entry per highlight colour plus one per non-default kind (' + keyItems + ' for kinds ' + kinds.join(',') + ')');
      // no-script / print fallback: the plain list must not show empty bullets for the edge markers
      await page.emulateMedia({ media: 'print' });
      const nestedShown = await page.evaluate(() => Array.from(document.querySelectorAll('ul.cm-graph ul')).filter((u) => getComputedStyle(u).display !== 'none').length);
      expect(nestedShown === 0, 'print: the nested edge lists of the fallback list are hidden (' + nestedShown + ' shown)');
      await page.emulateMedia({ media: 'screen' });
      // dimming must stay cheap with every folder expanded: handler plus two animation frames
      if (info.nodes >= 500) {
        for (;;) { const c = page.locator('g.cm-group.collapsed rect.cm-group-box').first(); if (!(await c.count())) break; await c.click(); }
        const frameMs = await page.evaluate(() => new Promise((resolve) => {
          const el = document.querySelector('g.cm-node[data-id="g1"]');
          const t0 = performance.now(); el.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
          requestAnimationFrame(() => requestAnimationFrame(() => resolve(performance.now() - t0)));
        }));
        result.hubFrameMs = Math.round(frameMs);
        expect(frameMs < 500, 'speed: with every folder expanded a hub hover took ' + Math.round(frameMs) + ' ms to reach the screen (limit 500, headless software rendering)');
      }
      // a folded graph can still be pinned once a folder is open
      if (folded) {
        await page.evaluate(() => document.querySelector('.cm-graph-panel') && 0);
        const open = page.locator('g.cm-group.collapsed rect.cm-group-box').first();
        if (await open.count()) await open.click();
        const visible = await page.evaluate(() => { const n = Array.from(document.querySelectorAll('g.cm-node')).find((g) => g.getBoundingClientRect().width > 0); return n ? n.getAttribute('data-id') : null; });
        expect(visible !== null, 'folded: an opened folder shows files');
        if (visible) {
          await page.locator('g.cm-node[data-id="' + visible + '"]').click();
          expect((await page.locator('.cm-graph-panel').innerText()).includes(rel[visible].path), 'folded: pinning a file in an opened folder fills the panel');
          await page.keyboard.press('Escape');
        }
      }
    }
  } catch (e) { failures.push('graph: check crashed: ' + String(e.message).split('\n').slice(0, 2).join(' ')); }

  if (deck) {
    expect(await page.locator('#cm-present').isVisible(), 'presentation button is visible');
    await page.click('#cm-present');
    await page.waitForTimeout(300);
    const first = await page.locator('#cm-count').textContent();
    await page.keyboard.press('ArrowRight');
    const second = await page.locator('#cm-count').textContent();
    await page.keyboard.press('End');
    const last = await page.locator('#cm-count').textContent();
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);
    result.deck = { first, second, last };
    expect(/^1 \/ \d+$/.test(first), 'deck starts at slide 1');
    expect(/^2 \/ \d+$/.test(second), 'ArrowRight moves to slide 2');
    expect(last.split(' / ')[0] === last.split(' / ')[1], 'End jumps to the last slide');
    expect(!(await page.evaluate(() => document.body.classList.contains('cm-presenting'))), 'Escape leaves presentation mode');
  }

  expect(errors.length === 0, 'no browser errors: ' + errors.join(' | '));
  await browser.close();
  console.log(JSON.stringify({ file, ...result, failures }));
  process.exit(failures.length ? 1 : 0);
})();
