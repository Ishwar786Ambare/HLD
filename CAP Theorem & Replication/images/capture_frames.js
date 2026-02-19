const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const HTML_FILE = path.resolve(__dirname, 'cap_animation.html');
const FRAMES_DIR = path.resolve(__dirname, 'frames');
const WIDTH = 1400;
const HEIGHT = 800;

// All looping animations run on a ~4s cycle.
// We capture 60 frames across one full 4000ms loop → 15 fps
const LOOP_DURATION_MS = 4000;
const NUM_FRAMES = 60;
const FRAME_STEP = LOOP_DURATION_MS / NUM_FRAMES;   // ~66.7 ms per frame

if (!fs.existsSync(FRAMES_DIR)) fs.mkdirSync(FRAMES_DIR);
fs.readdirSync(FRAMES_DIR).filter(f => f.endsWith('.png'))
    .forEach(f => fs.unlinkSync(path.join(FRAMES_DIR, f)));

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 2 });

    const fileUrl = `file:///${HTML_FILE.replace(/\\/g, '/')}`;
    await page.goto(fileUrl, { waitUntil: 'domcontentloaded' });

    // Wait a beat for all fonts/styles to settle
    await new Promise(r => setTimeout(r, 400));

    console.log(`Capturing ${NUM_FRAMES} frames of looping animation...`);

    for (let i = 0; i < NUM_FRAMES; i++) {
        // Advance all CSS animations to a point WITHIN their steady-state loop.
        // We offset by a large base (10000ms) so all fade-in delays are already done,
        // then step through one loop cycle.
        const t = 10000 + i * FRAME_STEP;

        await page.evaluate((ms) => {
            document.getAnimations().forEach(anim => {
                // Only control infinite looping animations (iteration count is Infinity)
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
