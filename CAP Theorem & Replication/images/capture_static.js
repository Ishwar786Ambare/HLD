const puppeteer = require('puppeteer');
const path = require('path');

const HTML_FILE = path.resolve(__dirname, 'cap_minimal.html');
const OUTPUT = path.resolve(__dirname, 'cap_minimal.png');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();

    // Start at the design width; scale factor 3 = crisp, high-res output
    await page.setViewport({ width: 1200, height: 900, deviceScaleFactor: 3 });

    const fileUrl = `file:///${HTML_FILE.replace(/\\/g, '/')}`;
    await page.goto(fileUrl, { waitUntil: 'networkidle0' });

    // Let fonts and layout settle
    await new Promise(r => setTimeout(r, 1500));

    // Measure actual page height and re-set viewport to match
    const bodyH = await page.evaluate(() => document.body.scrollHeight);
    await page.setViewport({ width: 1200, height: bodyH, deviceScaleFactor: 3 });
    await new Promise(r => setTimeout(r, 300));

    await page.screenshot({ path: OUTPUT, type: 'png', fullPage: true });
    await browser.close();
    console.log(`✅ Saved: ${OUTPUT}`);
})();
