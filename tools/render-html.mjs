// Render an HTML file to PNG at a fixed viewport. Usage: node tools/render-html.mjs in.html out.png [width] [height] [scale]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const [,, inFile, outFile, w = '1600', h = '1200', scale = '2'] = process.argv;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +scale });
await page.goto('file://' + (inFile.startsWith('/') ? inFile : process.cwd() + '/' + inFile));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(800);
await page.screenshot({ path: outFile, fullPage: false });
await browser.close();
console.log('wrote', outFile);
