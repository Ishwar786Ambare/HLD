const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
if (args.length < 5) {
    console.error("Usage: node capture_frames.js <html_file> <frames_dir> <width> <height> <loop_ms>");
    process.exit(1);
}

const HTML_FILE = path.resolve(args[0]);
const FRAMES_DIR = path.resolve(args[1]);
const WIDTH = parseInt(args[2]);
const HEIGHT = parseInt(args[3]);
const LOOP_DURATION_MS = parseInt(args[4]);
const NUM_FRAMES = 60; // Hardcoded to 60 for consistent ~5-second smooth loops
const FRAME_STEP = LOOP_DURATION_MS / NUM_FRAMES;

if (!fs.existsSync(FRAMES_DIR)) fs.mkdirSync(FRAMES_DIR, { recursive: true });
fs.readdirSync(FRAMES_DIR).filter(f => f.endsWith('.png')).forEach(f => fs.unlinkSync(path.join(FRAMES_DIR, f)));

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 2 });

    const fileUrl = `file:///${HTML_FILE.replace(/\\/g, '/')}`;
    await page.goto(fileUrl, { waitUntil: 'domcontentloaded' });

    // Wait for fonts to load
    await new Promise(r => setTimeout(r, 800));

    console.log(`Capturing ${NUM_FRAMES} frames...`);

    for (let i = 0; i < NUM_FRAMES; i++) {
        const t = 10000 + i * FRAME_STEP;

        await page.evaluate((ms) => {
            document.getAnimations().forEach(anim => {
                anim.currentTime = ms;
                anim.pause();
            });
        }, t);

        const framePath = path.join(FRAMES_DIR, `frame_${String(i).padStart(3, '0')}.png`);
        await page.screenshot({ path: framePath, type: 'png' });

        if (i % 10 === 0) console.log(`  Frame ${i + 1}/${NUM_FRAMES}`);
    }

    await browser.close();
    console.log('✅ Frames saved to:', FRAMES_DIR);
})();
