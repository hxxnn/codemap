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
        const hub = 'g1', h = rel[hub];
        await page.locator('g.cm-node[data-id="' + hub + '"]').hover();
        expect(JSON.stringify(await ids_of('g.cm-node.is-uses')) === JSON.stringify(h.uses.slice().sort()), 'focus: hover marks exactly the files the hovered file uses');
        expect(JSON.stringify(await ids_of('g.cm-node.is-usedby')) === JSON.stringify(h.usedBy.slice().sort()), 'focus: hover marks exactly the files that use the hovered file');
        expect((await ids_of('g.cm-node.is-focus')).join() === hub, 'focus: the hovered file is marked is-focus');
        const near = new Set([hub, ...h.uses, ...h.usedBy]);
        const others = ids.filter((i) => !near.has(i));
        expect(others.length > 0, 'focus: the fixture has files that are not direct neighbours');
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
