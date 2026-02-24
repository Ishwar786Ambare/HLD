const puppeteer = require('puppeteer');
const path = require('path');

const args = process.argv.slice(2);
if (args.length < 4) {
    console.error("Usage: node capture_static.js <html_file> <output_png> <width> <height>");
    process.exit(1);
}

const HTML_FILE = path.resolve(args[0]);
const OUTPUT_FILE = path.resolve(args[1]);
const WIDTH = parseInt(args[2]);
const HEIGHT = parseInt(args[3]);

(async () => {
    console.log(`Launching browser to capture static high-res image... (${WIDTH}x${HEIGHT})`);
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();

    // Use 2x scale for high quality
    await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 2 });

    const fileUrl = `file:///${HTML_FILE.replace(/\\/g, '/')}`;
    await page.goto(fileUrl, { waitUntil: 'domcontentloaded' });

    // Wait for fonts to load
    await new Promise(r => setTimeout(r, 1000));

    await page.screenshot({ path: OUTPUT_FILE, type: 'png' });

    await browser.close();
    console.log(`✅ Static high-res PNG saved to: ${OUTPUT_FILE}`);
})();
