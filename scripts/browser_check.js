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

  if (graph) {
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
    }
  }

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
