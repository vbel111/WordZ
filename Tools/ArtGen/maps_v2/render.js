// node render.js a.svg a.png [b.svg b.png ...]  -> renders SVGs at their own size with Chromium (Playwright).
// Uses Baloo2-ExtraBold.ttf next to this script as font-family "Baloo" when present. Transparent background.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const args = process.argv.slice(2);
  const fontPath = path.join(__dirname, 'Baloo2-ExtraBold.ttf');
  const font = fs.existsSync(fontPath) ? `@font-face{font-family:Baloo;src:url(data:font/ttf;base64,${fs.readFileSync(fontPath).toString('base64')})}` : '';
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (let i = 0; i + 1 < args.length; i += 2) {
    const svg = fs.readFileSync(args[i], 'utf8');
    const w = +svg.match(/width="(\d+)"/)[1], h = +svg.match(/height="(\d+)"/)[1];
    await page.setViewportSize({ width: w, height: h });
    await page.setContent(`<html><head><style>${font} html,body{margin:0;background:transparent}</style></head><body>${svg}</body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: args[i + 1], omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
  }
  await browser.close();
})();
