# -*- coding: utf-8 -*-
"""54 parasha pages: /parasha/<slug>/ – aliyot with chanted-audio links (Sefaria / PocketTorah), maftir and Sephardi haftarah
text with cantillation (Tanach with Ta'amei Hamikra – Public Domain), plus a book-by-book index injected into /parasha/."""
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

DATA = json.load(open(os.path.join(B.ROOT, "_build", "data", "parashot.json"), encoding="utf-8"))
BOOKS = {"Genesis": "בראשית", "Exodus": "שמות", "Leviticus": "ויקרא", "Numbers": "במדבר", "Deuteronomy": "דברים", "Joshua": "יהושע", "Judges": "שופטים",
         "I Samuel": "שמואל א", "II Samuel": "שמואל ב", "I Kings": "מלכים א", "II Kings": "מלכים ב", "Isaiah": "ישעיהו", "Jeremiah": "ירמיהו", "Ezekiel": "יחזקאל",
         "Hosea": "הושע", "Joel": "יואל", "Amos": "עמוס", "Obadiah": "עובדיה", "Jonah": "יונה", "Micah": "מיכה", "Nahum": "נחום", "Habakkuk": "חבקוק",
         "Zephaniah": "צפניה", "Haggai": "חגי", "Zechariah": "זכריה", "Malachi": "מלאכי"}
ALIYA = {"1": "ראשון", "2": "שני", "3": "שלישי", "4": "רביעי", "5": "חמישי", "6": "שישי", "7": "שביעי", "M": "מפטיר"}

def gem(n):
    n = int(n); o = ""
    for v, c in [(400,"ת"),(300,"ש"),(200,"ר"),(100,"ק"),(90,"צ"),(80,"פ"),(70,"ע"),(60,"ס"),(50,"נ"),(40,"מ"),(30,"ל"),(20,"כ"),(10,"י"),(9,"ט"),(8,"ח"),(7,"ז"),(6,"ו"),(5,"ה"),(4,"ד"),(3,"ג"),(2,"ב"),(1,"א")]:
        while n >= v:
            if n in (15, 16): return o + ("טו" if n == 15 else "טז")
            o += c; n -= v
    return o
def cv(x):
    p = str(x).split(":"); return gem(p[0]) + ("," + gem(p[1]) if len(p) > 1 else "")
def he_ref(book, b, e):
    e2 = e if ":" in e else f'{b.split(":")[0]}:{e}'
    return f'{BOOKS.get(book, book)} {cv(b)} – {cv(e2)}'
def he_haft(s):
    out, book = [], None
    for part in [p.strip() for p in (s or "").split(";") if p.strip()]:
        m = re.match(r"^([A-Za-z ]+?)\s+(\d+:\d+)(?:-(\d+(?::\d+)?))?$", part)
        if m:
            book = m.group(1); out.append(he_ref(book, m.group(2), m.group(3) or m.group(2)))
        else:
            m2 = re.match(r"^(\d+:\d+)(?:-(\d+(?::\d+)?))?$", part)
            if m2 and book: out.append(he_ref(book, m2.group(1), m2.group(2) or m2.group(1)).split(" ", 1)[1] if False else he_ref(book, m2.group(1), m2.group(2) or m2.group(1)))
    return "; ".join(out)
def slug(en): return re.sub(r"[^a-z0-9]+", "-", en.lower()).strip("-")
def listen(a):
    c, v = a["b"].split(":")
    return f'https://www.sefaria.org/{a["k"].replace(" ", "_")}.{c}.{v}?lang=he&with=Torah%20Readings'

def verses(lines, cls):
    return "".join(f'<p class="{cls}">{html.escape(t)}</p>' for t in (lines or []))

def page(p):
    s = slug(p["en"]); path = f"/parasha/{s}/"; he = p["he"]
    book = BOOKS.get(p["aliyot"][0]["k"], "") if p["aliyot"] else ""
    title = f"פרשת {he} לבר מצווה – עליות, מפטיר והפטרה בטעמים והאזנה"
    desc = f"פרשת {he} (ספר {book}): חלוקת העליות, המפטיר וההפטרה בנוסח ספרד ואשכנז, טקסט עם טעמי המקרא והאזנה לקריאה לכל עלייה. הכנה לבר מצווה עם ליאור ממו."
    rows = "".join(f'<tr><td><b>{ALIYA[a["n"]]}</b></td><td>{he_ref(a["k"], a["b"], a["e"])}</td><td>{a.get("v") or ""}</td>'
                   f'<td><a class="ls" href="{listen(a)}" target="_blank" rel="noopener" aria-label="האזנה לעלייה {ALIYA[a["n"]]}">▶ האזנה</a></td></tr>' for a in p["aliyot"])
    hs = he_haft(p.get("haftara_seph")); ha = he_haft(p.get("haftara_ashk"))
    hafts = f'<li><b>נוסח ספרד ועדות המזרח:</b> {hs}</li>' + (f'<li><b>נוסח אשכנז:</b> {ha}</li>' if ha and ha != hs else "")
    idx = next(i for i, x in enumerate(DATA) if x["num"] == p["num"])
    prev_, next_ = DATA[idx - 1] if idx > 0 else None, DATA[idx + 1] if idx + 1 < len(DATA) else None
    nav = '<div class="pnav">' + (f'<a href="/parasha/{slug(prev_["en"])}/">→ פרשת {prev_["he"]}</a>' if prev_ else "<span></span>") + \
          (f'<a href="/parasha/{slug(next_["en"])}/">פרשת {next_["he"]} ←</a>' if next_ else "") + '</div>'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": title, "description": desc, "inLanguage": "he", "url": B.SITE + path,
         "author": {"@id": B.BUSINESS_ID}, "publisher": {"@id": B.BUSINESS_ID}, "about": f"פרשת {he}"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ליאור ממו", "item": B.SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "פרשות השבוע", "item": B.SITE + "/parasha/"},
            {"@type": "ListItem", "position": 3, "name": f"פרשת {he}", "item": B.SITE + path}]}]}
    wa = B.urlq(f"שלום ליאור, הבר מצווה של הבן שלנו בפרשת {he} – נשמח לשמוע על הכנה ולימוד בטעמים")
    body = B.head(title, desc, path, ld) + B.sprite() + "\n\n" + B.nav("parasha") + f'''

<main id="top">
<section class="page-hero pr-hero">
  <div class="wrap" style="position:relative;z-index:1">
    <ol class="crumbs" aria-label="פירורי לחם"><li><a href="/">ליאור ממו</a></li><li><a href="/parasha/">פרשות השבוע</a></li><li aria-current="page">פרשת {he}</li></ol>
    <span class="label">ספר {book} · פרשה {p["num"]} מתוך 54</span>
    <h1>פרשת <em>{he}</em></h1>
    <p class="lede">כל מה שצריך לבר מצווה בפרשת {he}: חלוקת העליות עם האזנה לכל עלייה, המפטיר וההפטרה – עם טעמי המקרא.</p>
    <div class="hero-ctas"><a class="btn btn-solid" href="{B.WA}?text={wa}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>לימוד הפרשה עם ליאור</a><a class="btn btn-line" href="/parasha/">מחשבון הפרשה</a></div>
  </div>
</section>

<section class="pr-wrap">
  <div class="wrap pr-grid">
    <article class="pr-text ptext" id="prText" lang="he">
      <div class="pr-tools" role="toolbar" aria-label="כלי קריאה"><button type="button" data-fs="-1" aria-label="הקטנת גופן">א−</button><button type="button" data-fs="1" aria-label="הגדלת גופן">א+</button><button type="button" data-print>הדפסה</button><button type="button" data-share>שיתוף</button></div>
      <h2 class="pr-h">העליות בפרשה</h2>
      <p class="pr-note">לחצו על "האזנה" כדי לשמוע את קריאת העלייה בטעמים (נפתח באתר ספריא, הקלטות PocketTorah בנוסח אשכנז). ליאור מלמד את הקריאה בנוסח הטעמים של המשפחה.</p>
      <div class="tblwrap"><table class="aliyot"><thead><tr><th>עלייה</th><th>פסוקים</th><th>מס׳</th><th></th></tr></thead><tbody>{rows}</tbody></table></div>
      <h2 class="pr-h">המפטיר בטעמים</h2>
      {verses(p.get("maftir_text"), "pr-p")}
      {B_promo()}
      <h2 class="pr-h">ההפטרה</h2>
      <ul class="hafl">{hafts}</ul>
      <h3 class="pr-h3">נוסח ההפטרה (ספרד ועדות המזרח) בטעמים</h3>
      {verses(p.get("haftara_text"), "pr-p")}
      {nav}
      <p class="pr-src">הטקסט: תנ״ך עם טעמי המקרא (כתב יד לנינגרד, נחלת הכלל) באמצעות <a href="https://www.sefaria.org" target="_blank" rel="noopener">ספריא</a>. חלוקת העליות וההפטרות: <a href="https://www.hebcal.com" target="_blank" rel="noopener">Hebcal.com</a> (CC BY 4.0), לפי המנהג בישראל. ההקלטות שייכות למפיקיהן ומושמעות באתר ספריא.</p>
    </article>
    <aside class="pr-side">
      <div class="pr-cta">
        <span class="label">הכנה לבר מצווה</span>
        <h3>הבר מצווה בפרשת {he}?</h3>
        <p>ליאור ממו – חזן ובעל קורא – מלמד את הפרשה, המפטיר וההפטרה מילה במילה ובטעמים לפי מסורת המשפחה, ומלווה גם את העלייה לתורה עם נגנים.</p>
        <a class="btn btn-solid" href="/hachana-bar-mitzvah/">על ההכנה לבר מצווה</a>
        <a class="btn btn-line" href="{B.WA}?text={wa}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>וואטסאפ</a>
      </div>
      <nav class="pr-more" aria-label="פרשות נוספות"><b>ספר {book}</b>{"".join(f'<a href="/parasha/{slug(x["en"])}/">פרשת {x["he"]}</a>' for x in DATA if x["aliyot"] and BOOKS.get(x["aliyot"][0]["k"]) == book and x["num"] != p["num"])}</nav>
    </aside>
  </div>
</section>
</main>

{B.footer()}

{B.TAIL}

<script src="/js/site.js" defer></script>
<script src="/js/prayer.js" defer></script>
</body>
</html>
'''
    os.makedirs(os.path.join(B.ROOT, "parasha", s), exist_ok=True)
    open(os.path.join(B.ROOT, "parasha", s, "index.html"), "w", encoding="utf-8").write(body)
    return s

def B_promo():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import prayers as PR
    return PR.promo("hachana-bar-mitzvah")

def index_html():
    order = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]
    out = ['<section class="sec" id="all" style="padding-top:20px"><div class="wrap"><div class="sec-head"><div class="rv in"><span class="label">54 פרשות השבוע</span><h2 class="h2">כל הפרשות<br><em>בטעמים ובהאזנה.</em></h2></div><p class="lede">בחרו פרשה וקבלו את חלוקת העליות עם האזנה לכל עלייה, את המפטיר ואת ההפטרה – עם טעמי המקרא.</p></div>']
    for bk in order:
        items = [x for x in DATA if x["aliyot"] and x["aliyot"][0]["k"] == bk]
        out.append(f'<h3 class="pbook">ספר {BOOKS[bk]}</h3><div class="plist">' + "".join(f'<a href="/parasha/{slug(x["en"])}/">{x["he"]}</a>' for x in items) + '</div>')
    out.append('</div></section>')
    return "\n".join(out)

def inject_index():
    f = os.path.join(B.ROOT, "parasha", "index.html"); s = open(f, encoding="utf-8").read()
    s = re.sub(r'<section class="sec" id="all".*?</section>\n?', '', s, flags=re.S)
    anchor = '<section class="sec" style="padding-top:0">'
    s = s.replace(anchor, index_html() + "\n" + anchor, 1)
    open(f, "w", encoding="utf-8").write(s)

def slugs_map():
    return {x["en"]: slug(x["en"]) for x in DATA}

def add_to_sitemap():
    f = os.path.join(B.ROOT, "sitemap.xml"); s = open(f, encoding="utf-8").read()
    s = re.sub(r"\s*<url><loc>[^<]*/parasha/[a-z0-9-]+/</loc>.*?</url>", "", s, flags=re.S)
    urls = [f"  <url><loc>{B.SITE}/parasha/{slug(x['en'])}/</loc><lastmod>{B.UPLOAD}</lastmod><priority>0.6</priority></url>" for x in DATA]
    s = s.replace("</urlset>", "\n".join(urls) + "\n</urlset>")
    open(f, "w", encoding="utf-8").write(s)

def run():
    for p in DATA: page(p)
    inject_index(); add_to_sitemap()
    json.dump(slugs_map(), open(os.path.join(B.ROOT, "js", "parashot-map.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("parasha pages:", len(DATA))

if __name__ == "__main__": run()
