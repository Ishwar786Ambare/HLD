const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const svgFiles = [
    'caching_layers',
    'cache_aside_strategy',
    'write_strategies',
    'eviction_policies',
    'cache_problems',
    'consistent_hashing',
    'local_vs_distributed',
    'cdn_architecture'
];

(async () => {
    // Launch headless "new" for better performance in recent versions
    const browser = await puppeteer.launch({ headless: "new" });
    const page = await browser.newPage();

    for (const name of svgFiles) {
        const svgPath = path.resolve(__dirname, 'images', `${name}.svg`);
        const pngPath = path.resolve(__dirname, 'images', `${name}.png`);

        const svgContent = fs.readFileSync(svgPath, 'utf8');

        // Extract viewBox for dimensions
        const vbMatch = svgContent.match(/viewBox="([^"]+)"/);
        let width = 900, height = 500;
        if (vbMatch) {
            const parts = vbMatch[1].split(/\s+/);
            width = parseInt(parts[2]) || 900;
            height = parseInt(parts[3]) || 500;
        }

        // Use Scale 3 for High Quality (2700px width typically)
        await page.setViewport({ width, height, deviceScaleFactor: 3 });

        const html = `<!DOCTYPE html><html><head><style>body{margin:0;padding:0;}</style></head><body>${svgContent}</body></html>`;

        await page.setContent(html, { waitUntil: 'domcontentloaded', timeout: 30000 });
        // Explicit delay to ensure rendering is complete
        await new Promise(r => setTimeout(r, 200));

        await page.screenshot({ path: pngPath, type: 'png' });
        console.log(`PNG Created: ${name}.png`);
    }

    await browser.close();
})();
