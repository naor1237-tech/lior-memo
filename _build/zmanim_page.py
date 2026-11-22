# -*- coding: utf-8 -*-
"""/zmanim/ page (daily synagogue-style zmanim board + weekly Shabbat) and the home-page Shabbat bar."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

SHABBAT_BAR = '''<section class="shabbat-bar" id="shabbatBar" aria-label="זמני השבת הקרובה">
  <div class="wrap sb-in">
    <div class="sb-item sb-par"><small>פרשת השבוע</small><b data-z="par">…</b></div>
    <div class="sb-item sb-fri"><small>🕯️ כניסת שבת · <span data-z="city">ירושלים</span></small><b data-z="in">…</b></div>
    <div class="sb-item sb-fri"><small>✨ צאת שבת</small><b data-z="out">…</b></div>
    <div class="sb-item sb-week"><small>🌅 הנץ החמה · <span data-z="city2">ירושלים</span></small><b data-z="sunrise">…</b></div>
    <div class="sb-item sb-week"><small>📖 סוף זמן ק״ש (גר״א)</small><b data-z="shma">…</b></div>
    <div class="sb-item sb-week"><small>🌇 שקיעה</small><b data-z="sunset">…</b></div>
    <a class="sb-more" href="/zmanim/">לוח זמני היום ←</a>
  </div>
</section>'''

def page():
    path = "/zmanim/"
    title = "זמני היום ושבת – לוח זמנים יומי: זריחה, סוף זמן ק״ש, מנחה גדולה, שקיעה וצאת הכוכבים"
    desc = "לוח זמני היום כמו בבית הכנסת: עלות השחר, הנץ החמה, סוף זמן קריאת שמע ותפילה, חצות, מנחה גדולה וקטנה, פלג המנחה, שקיעה וצאת הכוכבים – וזמני כניסת ויציאת שבת ופרשת השבוע."
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": B.SITE + path, "inLanguage": "he"}
    body = B.head(title, desc, path, ld) + B.sprite() + "\n\n" + B.nav("zmanim") + f'''

<main id="top">
<section class="page-hero pr-hero">
  <div class="wrap" style="position:relative;z-index:1">
    <ol class="crumbs" aria-label="פירורי לחם"><li><a href="/">ליאור ממו</a></li><li aria-current="page">זמני היום</li></ol>
    <span class="label">לוח זמנים · מתעדכן אוטומטית</span>
    <h1>זמני <em>היום</em></h1>
    <p class="lede">לוח הזמנים כמו בבית הכנסת – עם שעון חי, הזמן הבא, וזמני השבת הקרובה ופרשת השבוע.</p>
  </div>
</section>
<section class="sec" style="padding-top:40px">
  <div class="wrap zgrid">
    <div class="zboard" id="zmanimBoard">
      <div class="zhead">
        <div><b data-z="hdate">…</b><span data-z="gdate"></span></div>
        <label class="zcity">עיר: <select data-z="picker" aria-label="בחירת עיר"></select></label>
      </div>
      <div class="zclock" data-z="clock" aria-live="off">--:--:--</div>
      <p class="znext" data-z="next"></p>
      <ul class="zlist" data-z="list"></ul>
      <p class="znote">הזמנים לפי Hebcal.com (רישיון CC BY 4.0). זמני ההלכה משתנים לפי השיטה – במקרה של ספק יש להתייעץ עם רב.</p>
    </div>
    <div class="zside">
      <div class="zshabbat" id="zmanimShabbat">
        <span class="label">השבת הקרובה</span>
        <div class="zs-row"><small>פרשת השבוע</small><b data-z="par">…</b></div>
        <div class="zs-row"><small>🕯️ כניסת שבת · <span data-z="city">ירושלים</span></small><b data-z="in">…</b></div>
        <div class="zs-row"><small>✨ צאת שבת</small><b data-z="out">…</b></div>
      </div>
      <div class="pr-cta" style="margin-top:20px">
        <span class="label">ליאור ממו · חזן ופייטן</span>
        <h3>חוגגים בר מצווה או שבת חתן?</h3>
        <p>חזנות, פיוטים ונגנים לשמחה – וליווי והכנה לבר מצווה בטעמים.</p>
        <a class="btn btn-solid" href="/bar-mitzvah/">לפרטים</a>
        <a class="btn btn-line" href="/parasha/">מה הפרשה של הבן?</a>
      </div>
    </div>
  </div>
</section>
</main>

{B.footer()}

{B.TAIL}

<script src="/js/site.js" defer></script>
<script src="/js/zmanim.js" defer></script>
</body>
</html>
'''
    os.makedirs(os.path.join(B.ROOT, "zmanim"), exist_ok=True)
    open(os.path.join(B.ROOT, "zmanim", "index.html"), "w", encoding="utf-8").write(body)

def patch_home():
    f = os.path.join(B.ROOT, "index.html"); s = open(f, encoding="utf-8").read()
    s = re.sub(r'<section class="shabbat-bar" id="shabbatBar".*?</section>\n?', '', s, flags=re.S)
    s = s.replace('<section class="statement">', SHABBAT_BAR + '\n\n<section class="statement">', 1)
    if '/js/zmanim.js' not in s:
        s = s.replace('<script src="/js/site.js', '<script src="/js/zmanim.js" defer></script>\n<script src="/js/site.js', 1)
    open(f, "w", encoding="utf-8").write(s)

def add_to_sitemap():
    f = os.path.join(B.ROOT, "sitemap.xml"); s = open(f, encoding="utf-8").read()
    if "/zmanim/" not in s:
        s = s.replace("</urlset>", f"  <url><loc>{B.SITE}/zmanim/</loc><lastmod>{B.UPLOAD}</lastmod><priority>0.6</priority></url>\n</urlset>")
    open(f, "w", encoding="utf-8").write(s)

def run():
    page(); patch_home(); add_to_sitemap(); print("zmanim built")

if __name__ == "__main__": run()
