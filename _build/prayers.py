# -*- coding: utf-8 -*-
"""Builds /tefilot/ prayer pages (not linked from the main navigation; reachable via search + sitemap).
Texts: Siddur Edot HaMizrach, Torat Emet edition (Public Domain) via Sefaria. Run: python _build/prayers.py"""
import json, os, re, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

DATA = json.load(open(os.path.join(B.ROOT, "_build", "data", "prayers.json"), encoding="utf-8"))

P = [  # slug, short name, title, description, intro, related service page
 ("birkat-hamazon","ברכת המזון","ברכת המזון – נוסח עדות המזרח (ספרדי) המלא, מנוקד",
  "ברכת המזון המלאה בנוסח עדות המזרח (ספרדי), מנוקדת וקריאה – כולל תוספות לשבת, ראש חודש וחגים. נוח לקריאה מהטלפון ולהדפסה.",
  "ברכת המזון נאמרת אחרי סעודה שאכלו בה לחם (כזית ומעלה). זהו הנוסח המלא לפי מנהג עדות המזרח, כולל ״רצה״ לשבת, ״יעלה ויבוא״ לראש חודש וחגים, ו״על הניסים״ לחנוכה ופורים.","bar-mitzvah"),
 ("meein-shalosh","ברכה מעין שלוש","ברכה מעין שלוש (על המחיה) – נוסח עדות המזרח, מנוקד",
  "ברכה מעין שלוש – על המחיה, על הגפן ועל העץ – בנוסח עדות המזרח, מנוקדת ומלאה. מתי אומרים אותה ומה מוסיפים בשבת וחג.",
  "ברכה מעין שלוש נאמרת אחרי אכילת מזונות (עוגות, פת הבאה בכיסנין), שתיית יין, או אכילת פירות משבעת המינים. זהו הנוסח המלא לפי מנהג עדות המזרח.","bar-mitzvah"),
 ("tefilat-haderech","תפילת הדרך","תפילת הדרך – הנוסח המלא, מנוקד (עדות המזרח)",
  "תפילת הדרך המלאה והמנוקדת בנוסח עדות המזרח – לנסיעה, לטיסה ולכל יציאה לדרך. נוח לקריאה מהטלפון.",
  "תפילת הדרך נאמרת כשיוצאים לדרך מחוץ לעיר. זהו הנוסח המלא לפי מנהג עדות המזרח – שמרו את העמוד בטלפון לנסיעה הבאה.","shabbat-chatan"),
 ("kiddush-leil-shabbat","קידוש לליל שבת","קידוש לליל שבת – נוסח עדות המזרח המלא, מנוקד",
  "קידוש לליל שבת בנוסח עדות המזרח (ספרדי) – ״ויכולו״ והקידוש המלא, מנוקד וקריא. מושלם לשולחן השבת ולשבת חתן.",
  "הקידוש נאמר בליל שבת על כוס יין לפני הסעודה. זהו הנוסח המלא לפי מנהג עדות המזרח.","shabbat-chatan"),
 ("shalom-aleichem","שלום עליכם","שלום עליכם – מילים מלאות ומנוקדות (נוסח עדות המזרח)",
  "שלום עליכם מלאכי השרת – המילים המלאות והמנוקדות לשירה בליל שבת, בנוסח עדות המזרח.",
  "״שלום עליכם״ שרים בליל שבת בכניסה הביתה מבית הכנסת, לפני הקידוש – לקבל את מלאכי השבת.","shabbat-chatan"),
 ("eshet-chayil","אשת חיל","אשת חיל מי ימצא – מילים מלאות ומנוקדות",
  "אשת חיל מי ימצא – המילים המלאות והמנוקדות (משלי ל״א), כפי שנוהגים לשיר בליל שבת.",
  "״אשת חיל״ – הפרק האחרון בספר משלי – נהוג לשיר בליל שבת לפני הקידוש, לכבוד עקרת הבית.","shabbat-chatan"),
 ("birkat-habanim","ברכת הבנים","ברכת הבנים בליל שבת – הנוסח המלא והמנוקד",
  "ברכת הבנים והבנות בליל שבת – ״ישימך אלהים כאפרים וכמנשה״ וברכת כהנים, בנוסח עדות המזרח, מנוקד.",
  "בליל שבת נוהגים ההורים לברך את הילדים בברכת הבנים. זהו הנוסח לפי מנהג עדות המזרח.","bar-mitzvah"),
 ("havdala","הבדלה","סדר הבדלה במוצאי שבת – נוסח עדות המזרח המלא, מנוקד",
  "סדר הבדלה למוצאי שבת בנוסח עדות המזרח – הפסוקים, ברכת היין, הבשמים והנר, וברכת המבדיל. מנוקד ונוח לקריאה.",
  "בהבדלה נפרדים מהשבת במוצאי שבת, על כוס יין, בשמים ונר. זהו הסדר המלא לפי מנהג עדות המזרח.","shabbat-chatan"),
 ("hadlakat-nerot","הדלקת נרות שבת","ברכת הדלקת נרות שבת – הנוסח והתפילה, מנוקד",
  "ברכת הדלקת נרות שבת והתפילה שאחריה, בנוסח עדות המזרח, מנוקדת.",
  "את נרות השבת מדליקים לפני כניסת השבת, ומברכים ״להדליק נר של שבת״. זהו הנוסח לפי מנהג עדות המזרח.","shabbat-chatan"),
 ("sheva-brachot","שבע ברכות","שבע ברכות – הנוסח המלא והמנוקד (חתונה ושבע ברכות)",
  "שבע הברכות המלאות והמנוקדות – הנאמרות בחופה ובסעודות שבע ברכות – בנוסח עדות המזרח.",
  "שבע ברכות נאמרות תחת החופה, ובכל סעודה חגיגית בשבוע שאחרי החתונה. זהו הנוסח המלא לפי מנהג עדות המזרח.","shabbat-chatan"),
 ("kriat-shema-al-hamita","קריאת שמע על המיטה","קריאת שמע על המיטה – נוסח עדות המזרח המלא, מנוקד",
  "קריאת שמע שעל המיטה המלאה והמנוקדת בנוסח עדות המזרח – לפני השינה, למבוגרים ולילדים.",
  "קריאת שמע שעל המיטה נאמרת לפני השינה. זהו הנוסח המלא לפי מנהג עדות המזרח.","hachana-bar-mitzvah"),
 ("birkot-hanehenin","ברכות הנהנין","ברכות הנהנין – ברכות ראשונות על מאכלים ומשקאות",
  "ברכות הנהנין: המוציא, מזונות, הגפן, העץ, האדמה ושהכל – הנוסח המנוקד לפי מנהג עדות המזרח.",
  "ברכות הנהנין הן הברכות שמברכים לפני אכילה ושתייה. כאן תמצאו את הנוסח לכל סוג מאכל, לפי מנהג עדות המזרח.","hachana-bar-mitzvah"),
]
SERVICE_CTA = {
 "bar-mitzvah":("חוגגים בר מצווה?","ליאור ממו – חזן, פייטן ונגן עוד – הופך את העלייה לתורה לחגיגה עם פיוטים ונגנים."),
 "shabbat-chatan":("מתכננים שבת חתן או שבע ברכות?","ליאור ממו מביא חזנות, פיוטים ושירי שבת שכל השולחן מצטרף אליהם."),
 "hachana-bar-mitzvah":("מתכוננים לבר מצווה?","ליאור ממו, חזן ובעל קורא, מלמד קריאה בתורה, טעמים והפטרה – בסבלנות ובגובה העיניים."),
}

ALLOWED = {"b","big","small","i","br","strong","em"}
def clean(s):
    s = re.sub(r"<(/?)(\w+)[^>]*>", lambda m: f"<{m.group(1)}{m.group(2).lower()}>" if m.group(2).lower() in ALLOWED else "", s)
    return s.strip()

def render(text):
    out = []
    def walk(t):
        if isinstance(t, list):
            for x in t: walk(x)
        elif isinstance(t, str) and t.strip():
            c = clean(t)
            plain = re.sub(r"<[^>]+>", "", c).strip()
            if re.fullmatch(r"<big>\s*(<b>)?[^<]{1,60}(</b>)?\s*</big>", c):
                out.append(f'<h2 class="pr-h">{plain}</h2>')
            elif c.startswith("<small>") and c.endswith("</small>") and c.count("<small>") == 1:
                inner = c[7:-8]
                out.append(f'<p class="pr-note">{inner}</p>' if len(plain) < 160 and not re.search(r"[ְ-ּ]", plain) else f'<p class="pr-p pr-sm">{inner}</p>')
            else:
                out.append(f'<p class="pr-p">{c}</p>')
    walk(text)
    return "\n".join(out)

def first_words(text, n=40):
    flat = []
    def walk(t):
        if isinstance(t, list):
            for x in t: walk(x)
        elif isinstance(t, str): flat.append(re.sub(r"<[^>]+>", " ", t))
    walk(text)
    s = re.sub(r"[֑-ׇ]", "", " ".join(flat)); s = re.sub(r"\s+", " ", s).strip()
    return " ".join(s.split(" ")[:n])

TOOLS = '''<div class="pr-tools" role="toolbar" aria-label="כלי קריאה">
  <button type="button" data-fs="-1" aria-label="הקטנת גופן">א−</button>
  <button type="button" data-fs="1" aria-label="הגדלת גופן">א+</button>
  <button type="button" data-print aria-label="הדפסה">הדפסה</button>
  <button type="button" data-share aria-label="שיתוף בוואטסאפ">שיתוף</button>
</div>'''

def page(item):
    slug, name, title, desc, intro, svc = item
    d = DATA[slug]; path = f"/tefilot/{slug}/"
    others = "".join(f'<a href="/tefilot/{s}/">{n}</a>' for s,n,*_ in P if s != slug)
    cta_t, cta_d = SERVICE_CTA[svc]
    svc_name = next(p["nav"] for p in B.PAGES if p["slug"] == svc)
    ld = {"@context":"https://schema.org","@graph":[
        {"@type":"WebPage","name":title,"description":desc,"url":B.SITE+path,"inLanguage":"he",
         "isPartOf":{"@type":"WebSite","name":"ליאור ממו – חזן ופייטן","url":B.SITE+"/"},
         "mainEntity":{"@type":"CreativeWork","name":name,"inLanguage":"he","license":"https://creativecommons.org/publicdomain/mark/1.0/",
                       "isBasedOn":"https://www.sefaria.org/"+d["ref"].replace(" ","_"),"text":first_words(d["text"])}},
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"ליאור ממו","item":B.SITE+"/"},
            {"@type":"ListItem","position":2,"name":"תפילות וברכות","item":B.SITE+"/tefilot/"},
            {"@type":"ListItem","position":3,"name":name,"item":B.SITE+path}]}]}
    body = B.head(title, desc, path, ld) + B.sprite() + "\n\n" + B.nav("") + f'''

<main id="top" class="prayer">
<section class="page-hero pr-hero">
  <div class="wrap" style="position:relative;z-index:1">
    <ol class="crumbs" aria-label="פירורי לחם"><li><a href="/">ליאור ממו</a></li><li><a href="/tefilot/">תפילות וברכות</a></li><li aria-current="page">{name}</li></ol>
    <span class="label">נוסח עדות המזרח · מנוקד</span>
    <h1>{name}</h1>
    <p class="lede">{intro}</p>
  </div>
</section>

<section class="pr-wrap">
  <div class="wrap pr-grid">
    <article class="pr-text" id="prText" lang="he">
      {TOOLS}
      {render(d["text"])}
      <p class="pr-src">הנוסח: סידור עדות המזרח, מהדורת ״תורת אמת״ (נחלת הכלל), באמצעות <a href="https://www.sefaria.org/{d["ref"].replace(" ","_")}" target="_blank" rel="noopener">ספריא</a>. ייתכנו הבדלי מנהג בין קהילות.</p>
    </article>
    <aside class="pr-side">
      <div class="pr-cta">
        <span class="label">ליאור ממו · חזן ופייטן</span>
        <h3>{cta_t}</h3>
        <p>{cta_d}</p>
        <a class="btn btn-solid" href="/{svc}/">{svc_name}</a>
        <a class="btn btn-line" href="{B.WA}?text={B.urlq('שלום ליאור, הגעתי מהאתר (עמוד ' + name + ')')}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>וואטסאפ</a>
      </div>
      <nav class="pr-more" aria-label="תפילות נוספות"><b>תפילות וברכות נוספות</b>{others}</nav>
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
    out = os.path.join(B.ROOT, "tefilot", slug); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(body)

def hub():
    path = "/tefilot/"
    title = "תפילות וברכות בנוסח עדות המזרח – ברכת המזון, קידוש, הבדלה ועוד"
    desc = "אוסף תפילות וברכות מנוקדות בנוסח עדות המזרח: ברכת המזון, ברכה מעין שלוש, תפילת הדרך, קידוש, הבדלה, שבע ברכות ועוד – נוחות לקריאה מהטלפון."
    cards = "".join(f'<a class="rel rv" href="/tefilot/{s}/"><small>נוסח עדות המזרח</small><b>{n}</b><span>{d[:70]}…</span></a>' for s,n,t,d,*_ in P)
    ld = {"@context":"https://schema.org","@graph":[
        {"@type":"CollectionPage","name":title,"description":desc,"url":B.SITE+path,"inLanguage":"he",
         "hasPart":[{"@type":"WebPage","name":n,"url":f"{B.SITE}/tefilot/{s}/"} for s,n,*_ in P]},
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"ליאור ממו","item":B.SITE+"/"},
            {"@type":"ListItem","position":2,"name":"תפילות וברכות","item":B.SITE+path}]}]}
    body = B.head(title, desc, path, ld) + B.sprite() + "\n\n" + B.nav("") + f'''

<main id="top">
<section class="page-hero pr-hero">
  <div class="wrap" style="position:relative;z-index:1">
    <ol class="crumbs" aria-label="פירורי לחם"><li><a href="/">ליאור ממו</a></li><li aria-current="page">תפילות וברכות</li></ol>
    <span class="label">נוסח עדות המזרח · מנוקד</span>
    <h1>תפילות <em>וברכות</em></h1>
    <p class="lede">ברכת המזון, קידוש, הבדלה, שבע ברכות ועוד – מנוקדות ונוחות לקריאה מהטלפון, באדיבות ליאור ממו, חזן ופייטן.</p>
  </div>
</section>
<section class="sec"><div class="wrap"><div class="related">{cards}</div></div></section>
{B.cta()}
</main>

{B.footer()}

{B.TAIL}

<script src="/js/site.js" defer></script>
</body>
</html>
'''
    os.makedirs(os.path.join(B.ROOT, "tefilot"), exist_ok=True)
    open(os.path.join(B.ROOT, "tefilot", "index.html"), "w", encoding="utf-8").write(body)

def add_to_sitemap():
    f = os.path.join(B.ROOT, "sitemap.xml"); s = open(f, encoding="utf-8").read()
    s = re.sub(r"\s*<url><loc>[^<]*/tefilot/[^<]*</loc>.*?</url>", "", s, flags=re.S)
    urls = [f"  <url><loc>{B.SITE}/tefilot/</loc><lastmod>{B.UPLOAD}</lastmod><priority>0.6</priority></url>"]
    urls += [f"  <url><loc>{B.SITE}/tefilot/{p[0]}/</loc><lastmod>{B.UPLOAD}</lastmod><priority>0.7</priority></url>" for p in P]
    s = s.replace("</urlset>", "\n".join(urls) + "\n</urlset>")
    open(f, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    for item in P: page(item)
    hub(); add_to_sitemap()
    print("prayers:", len(P))
