// node render.js work_dir [step] [from] [to]  -> work_dir/frames/f00000.jpg ... (30 fps)
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const dir = path.resolve(process.argv[2]);
  const step = +(process.argv[3] || 1), from = +(process.argv[4] || 0);
  const data = JSON.parse(fs.readFileSync(path.join(dir, 'data.json'), 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.addInitScript(d => { window.DATA = d; }, data);
  await page.goto('file://' + path.join(dir, 'trailer.html'));
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; })));
    // make sure CSS background images are decoded too
    const urls = ['pano.png', 'map_city.jpg', 'map_ocean.jpg', 'map_space.jpg', 'map_halloween.jpg', 'bg_city.jpg', 'bg_space.jpg'];
    await Promise.all(urls.map(u => new Promise(r => { const i = new Image(); i.onload = i.onerror = r; i.src = 'assets/' + u; })));
  });
  const { FPS, DURATION } = await page.evaluate(() => window.TRAILER);
  const total = Math.round(FPS * DURATION);
  const to = +(process.argv[5] || total);
  fs.mkdirSync(path.join(dir, 'frames'), { recursive: true });
  const stage = await page.$('#stage');
  for (let i = from; i < to; i += step) {
    await page.evaluate(t => window.render(t), i / FPS);
    await stage.screenshot({ path: path.join(dir, 'frames', `f${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 93 });
  }
  await browser.close();
  console.log('frames', from, to, step);
})();
