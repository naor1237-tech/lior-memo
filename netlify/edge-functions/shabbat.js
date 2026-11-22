// "Shomer Shabbat": during Shabbat and Israeli Yom Tov (Jerusalem times, from Hebcal) every page request gets a
// closed page with the reopening time; it reloads itself the moment Shabbat/Yom Tov ends. Fails open if Hebcal is unreachable.
// Preview anytime with ?shabbat-preview=1
const GEO = 281184; // Jerusalem
let cache = { at: 0, windows: [] };

function iso(d) { return d.toISOString().slice(0, 10); }

async function getWindows() {
  const now = Date.now();
  if (now - cache.at < 3 * 3600 * 1000 && cache.windows.length) return cache.windows;
  const start = new Date(now - 3 * 864e5), end = new Date(now + 10 * 864e5);
  const url = `https://www.hebcal.com/hebcal?v=1&cfg=json&maj=on&c=on&i=on&geonameid=${GEO}&b=40&M=on&start=${iso(start)}&end=${iso(end)}`;
  const res = await fetch(url, { headers: { "accept": "application/json" } });
  if (!res.ok) throw new Error("hebcal " + res.status);
  const items = (await res.json()).items || [];
  const ev = items.filter(i => i.category === "candles" || i.category === "havdalah")
                  .map(i => ({ t: Date.parse(i.date), k: i.category, title: i.hebrew || i.title }))
                  .sort((a, b) => a.t - b.t);
  const holidays = items.filter(i => i.category === "holiday" && (i.yomtov || /^(Rosh Hashana|Yom Kippur|Pesach I|Pesach VII|Shavuot|Sukkot I|Shmini Atzeret)/.test(i.title)));
  const windows = [];
  for (let i = 0; i < ev.length; i++) {
    if (ev[i].k !== "candles") continue;
    const close = ev.slice(i + 1).find(e => e.k === "havdalah");
    if (!close) continue;
    const day = new Date(close.t);
    const hol = holidays.find(h => Math.abs(Date.parse(h.date) - ev[i].t) < 2.2 * 864e5);
    windows.push({ from: ev[i].t, to: close.t, holiday: hol ? (hol.hebrew || hol.title) : null, sat: day.getUTCDay() === 6 });
    // merge consecutive windows (Shabbat next to Yom Tov): skip candles that fall inside an open window
    while (i + 1 < ev.length && ev[i + 1].t < close.t) i++;
  }
  cache = { at: now, windows };
  return windows;
}

const fmt = (t) => new Intl.DateTimeFormat("he-IL", { timeZone: "Asia/Jerusalem", hour: "2-digit", minute: "2-digit", hour12: false }).format(new Date(t));
const fmtDay = (t) => new Intl.DateTimeFormat("he-IL", { timeZone: "Asia/Jerusalem", weekday: "long", day: "numeric", month: "long" }).format(new Date(t));

function page(w, preview) {
  const name = w.holiday ? (w.sat ? "שבת וחג" : "חג") : "שבת";
  const greet = w.holiday ? (w.sat ? "שבת שלום וחג שמח" : "חג שמח") : "שבת שלום";
  return `<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${greet} – האתר שומר שבת וחגי ישראל · ליאור ממו</title><meta name="robots" content="noindex">
<style>
*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;background:radial-gradient(ellipse at 50% 0%,rgba(201,169,106,.18),transparent 60%),#0b0a09;color:#f3ece0;font-family:Assistant,Arial,sans-serif;text-align:center;padding:24px}
.c{max-width:560px}.dia{width:14px;height:14px;background:#c9a96a;transform:rotate(45deg);margin:0 auto 22px}
.cn{font-size:56px;line-height:1;margin-bottom:10px}
h1{font-family:"Suez One",Georgia,serif;font-weight:400;font-size:44px;color:#e6cf9a;margin:0 0 10px;line-height:1.1}
p{color:#cfc6b8;font-size:18px;line-height:1.7;margin:0 0 8px}
.t{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:26px 0}
.t div{border:1px solid rgba(201,169,106,.4);border-radius:14px;padding:16px}
.t small{display:block;color:#c9a96a;font-size:13px;letter-spacing:.1em}.t b{font-size:30px;font-family:Georgia,serif;color:#fff}
.cd{font-size:15px;color:#a39a8c;margin-top:8px}.cd b{color:#e6cf9a}
.n{margin-top:30px;color:#8a8274;font-size:14px}.pv{position:fixed;top:0;inset-inline:0;background:#c9a96a;color:#000;padding:6px;font-size:13px;font-weight:700}
</style></head><body>${preview ? '<div class="pv">תצוגה מקדימה של מצב שבת</div>' : ""}
<main class="c"><div class="cn" aria-hidden="true">🕯️🕯️</div><div class="dia"></div>
<h1>${greet}!</h1>
<p>האתר של ליאור ממו <b>שומר שבת וחגי ישראל</b>${w.holiday ? ` – ${w.holiday}` : ""}.</p>
<p>נשמח לעמוד לשירותכם מיד בצאת ה${name}.</p>
<div class="t"><div><small>כניסת ה${name}</small><b>${fmt(w.from)}</b><div class="cd">${fmtDay(w.from)}</div></div><div><small>צאת ה${name} – האתר נפתח</small><b>${fmt(w.to)}</b><div class="cd">${fmtDay(w.to)}</div></div></div>
<p class="cd" id="cd">האתר ייפתח אוטומטית בעוד <b id="left">…</b></p>
<p class="n">זמני ירושלים · ליאור ממו – חזן, פייטן, בעל קורא ונגן עוד</p></main>
<script>var to=${w.to};function tick(){var s=Math.max(0,Math.round((to-Date.now())/1000));var h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=s%60;document.getElementById('left').textContent=(h?h+':':'')+String(m).padStart(2,'0')+':'+String(x).padStart(2,'0');if(s<=0){location.reload();}}tick();setInterval(tick,1000);</script>
</body></html>`;
}

export default async (request, context) => {
  const url = new URL(request.url);
  const preview = url.searchParams.has("shabbat-preview");
  let w = null;
  try {
    const now = Date.now();
    const windows = await getWindows();
    w = windows.find(x => now >= x.from && now < x.to) || null;
    if (!w && preview) w = windows.find(x => x.from > now) || null;
  } catch (e) {
    return; // fail open – show the site
  }
  if (!w) return; // not Shabbat / Yom Tov – continue to the static site
  const retry = Math.max(60, Math.round((w.to - Date.now()) / 1000));
  return new Response(page(w, preview), {
    status: preview ? 200 : 503,
    headers: { "content-type": "text/html; charset=utf-8", "retry-after": String(retry), "cache-control": "no-store" },
  });
};

export const config = {
  path: "/*",
  excludedPath: ["/media/*", "/css/*", "/js/*", "/v/*", "/files/*", "/robots.txt", "/sitemap.xml", "/*.txt", "/googlea390d3271dac40cd.html", "/favicon.svg"],
};
