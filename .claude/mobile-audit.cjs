#!/usr/bin/env node
/**
 * בדיקת מובייל: כל דף HTML בפרויקט ב-320, 375 ו-768 פיקסלים.
 * נכשל על: גלילה הצידה (משהו יוצא מהמסך) או דף בלי <meta name="viewport" content="width=device-width">.
 *
 *   node .claude/mobile-audit.cjs              ← כל הדפים
 *   node .claude/mobile-audit.cjs about.html   ← דפים מסוימים
 *
 * צריך Playwright (מותקן בסביבת הענן). דפים שמפנים לדף אחר, תבניות לייצוא תמונה וקטעים שנטענים בתוך
 * דף אחר מדלגים עליהם ב-SKIP. יוצא עם קוד 1 כשיש בעיה, ומדפיס את האלמנט שיוצא מהמסך.
 */
'use strict';
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path'), { execSync } = require('child_process');

const ROOT = process.cwd();
const SKIP = /(^|\/)(node_modules|marketing|_audit|_build|tests?|docs|graphify-out|\.claude|brand\/source|scripts|notebooklm|handoff|content\/video|content\/course\/scoler|netlify\/functions\/_data)\/|(^|\/)google[0-9a-f]+\.html$/;
const VPS = [{ name: '320', width: 320, height: 640 }, { name: '375', width: 375, height: 740 }, { name: '768', width: 768, height: 1024 }];
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.json': 'application/json', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf' };

const args = process.argv.slice(2);
const files = (args.length ? args : execSync('git -c core.quotePath=false ls-files "*.html"', { cwd: ROOT }).toString().split('\n')).filter(f => f && !SKIP.test(f));

const srv = http.createServer((q, r) => {
  let f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
  try { if (fs.statSync(f).isDirectory()) f = path.join(f, 'index.html'); } catch { if (fs.existsSync(f + '.html')) f += '.html'; }
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); r.end(d); });
}).listen(0);
const base = `http://127.0.0.1:${srv.address().port}/`;

(async () => {
  // גרסת Playwright של הפרויקט יכולה להיות שונה מהדפדפן המותקן: אז הדפדפן המשותף של הסביבה
  const browser = await chromium.launch().catch(() => chromium.launch({ executablePath: process.env.PW_CHROMIUM || '/opt/pw-browsers/chromium' }));
  const ctx = {};
  for (const v of VPS) ctx[v.name] = await browser.newContext({ viewport: { width: v.width, height: v.height }, isMobile: true, hasTouch: true });
  const bad = []; let i = 0;
  async function worker() {
    while (i < files.length) {
      const f = files[i++]; const html = fs.readFileSync(path.join(ROOT, f), 'utf8');
      if (/http-equiv=["']?refresh|location\.replace\(/i.test(html)) continue; // דף הפניה
      if (!/<html[\s>]/i.test(html)) continue; // קטע HTML שנטען בתוך דף אחר, לא דף שלם
      const probs = [];
      if (!/<meta[^>]+name=["']viewport["'][^>]*width=device-width/i.test(html)) probs.push('no viewport meta');
      for (const v of VPS) {
        const p = await ctx[v.name].newPage();
        await p.goto(base + f, { waitUntil: 'load', timeout: 15000 }).catch(() => {});
        await p.waitForTimeout(800);
        const r = await p.evaluate(() => {
          const vw = document.documentElement.clientWidth, over = document.documentElement.scrollWidth - vw;
          if (over <= 1) return null;
          const out = [];
          for (const el of document.querySelectorAll('body *')) {
            if (el.children.length) continue;
            const b = el.getBoundingClientRect();
            if (b.width && (b.right > vw + 1 || b.left < -1)) out.push(`${el.tagName.toLowerCase()}${el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/)[0] : ''} "${(el.textContent || '').trim().slice(0, 25)}"`);
          }
          return `+${over}px ${out.slice(0, 2).join(' ; ')}`;
        }).catch(() => null);
        if (r) probs.push(`${v.name}px: ${r}`);
        await p.close();
      }
      if (probs.length) bad.push(`${f}\n    ${probs.join('\n    ')}`);
    }
  }
  await Promise.all(Array.from({ length: 4 }, worker));
  await browser.close(); srv.close();
  if (bad.length) { console.log(`✗ ${bad.length} מתוך ${files.length} דפים לא מתאימים לטלפון:\n  ${bad.join('\n  ')}`); process.exit(1); }
  console.log(`✓ כל ${files.length} הדפים מתאימים ל-320, 375 ו-768 פיקסלים`);
})();
