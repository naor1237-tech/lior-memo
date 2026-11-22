# -*- coding: utf-8 -*-
"""Branded 404 page (Netlify serves /404.html for any missing path)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

def run():
    title = "העמוד לא נמצא – ליאור ממו"
    desc = "העמוד שחיפשתם לא נמצא. חזרו לדף הבית של ליאור ממו – חזן, פייטן, בעל קורא ונגן עוד."
    s = B.head(title, desc, "/404.html", {"@context": "https://schema.org", "@type": "WebPage", "name": title})
    s = s.replace('<meta name="robots" content="index,follow', '<meta name="robots" content="noindex,follow')
    s = __import__("re").sub(r'<link rel="canonical"[^>]*>\n?', '', s)
    if 'name="robots"' not in s: s = s.replace("</head>", '<meta name="robots" content="noindex">\n</head>', 1)
    s += B.sprite() + "\n\n" + B.nav("") + f'''

<main id="top">
<section class="page-hero pr-hero">
  <div class="wrap" style="position:relative;z-index:1;text-align:center">
    <span class="label">שגיאה 404</span>
    <h1>העמוד <em>לא נמצא</em></h1>
    <p class="lede" style="margin-inline:auto">ייתכן שהקישור השתנה. הנה כמה מקומות טובים להמשיך מהם:</p>
    <div class="hero-ctas" style="justify-content:center;flex-wrap:wrap">
      <a class="btn btn-solid" href="/">לדף הבית</a>
      <a class="btn btn-line" href="/parasha/">מחשבון הפרשה</a>
      <a class="btn btn-line" href="/tefilot/">תפילון</a>
      <a class="btn btn-line" href="/zmanim/">זמני היום</a>
      <a class="btn btn-line" href="{B.WA}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>וואטסאפ לליאור</a>
    </div>
  </div>
</section>
</main>

{B.footer()}

{B.TAIL}

<script src="/js/site.js" defer></script>
</body>
</html>
'''
    open(os.path.join(B.ROOT, "404.html"), "w", encoding="utf-8").write(s)
    print("404 built")

if __name__ == "__main__": run()
