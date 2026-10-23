// Renders every svg/*.svg to png/*.png at the svg's width/height with a transparent background.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const dir = path.join(__dirname, 'svg'), out = path.join(__dirname, 'png');
  const font = fs.readFileSync(path.join(__dirname, 'Baloo2-ExtraBold.ttf')).toString('base64');
  const only = process.argv[2];
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg') && (!only || f.includes(only)))) {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8');
    const w = +svg.match(/width="(\d+)"/)[1], h = +svg.match(/height="(\d+)"/)[1];
    await page.setViewportSize({ width: w, height: h });
    await page.setContent(`<html><head><style>@font-face{font-family:Baloo;src:url(data:font/ttf;base64,${font})}
      html,body{margin:0;padding:0;background:transparent}svg{display:block}</style></head><body>${svg}</body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(out, f.replace('.svg', '.png')), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
  }
  await browser.close();
})();
