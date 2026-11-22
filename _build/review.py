# -*- coding: utf-8 -*-
"""/review/ – one short link Lior sends to every client. Set GOOGLE_REVIEW_URL once the Business Profile is verified."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

GOOGLE_REVIEW_URL = ""  # e.g. "https://g.page/r/XXXX/review"  ← paste from Google Business Profile → "Ask for reviews"

def page():
    msg = "שלום ליאור! רציתי לשתף איך היה לנו באירוע:\n\n[כתבו כאן כמה מילים]\n\nשם: \nסוג האירוע: \nמותר לפרסם באתר? כן / לא"
    google_btn = (f'<a class="btn btn-solid" href="{GOOGLE_REVIEW_URL}" target="_blank" rel="noopener">★ כתיבת ביקורת בגוגל</a>'
                  if GOOGLE_REVIEW_URL else "")
    body = B.head("תודה! ספרו איך היה – ליאור ממו", "שיתוף חוויה מאירוע עם ליאור ממו, חזן ופייטן.", "/review/", {"@context":"https://schema.org","@type":"WebPage","name":"ביקורת"}) \
        .replace('<meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1">', '<meta name="robots" content="noindex,follow">') \
        + B.sprite() + "\n\n" + B.nav("") + f'''

<main id="top">
<section class="page-hero" style="min-height:100svh;display:flex;align-items:center">
  <div class="hero-bg" aria-hidden="true"><img src="/media/hero.jpg" alt=""></div>
  <div class="wrap" style="position:relative;z-index:1;text-align:center;max-width:760px">
    <div class="orn"><svg><use href="#i-dia"/></svg></div>
    <h1>תודה שהייתי<br><em>חלק מהשמחה.</em></h1>
    <p class="lede" style="margin:0 auto">אם נהניתם – כמה מילים מכם עוזרות לי להגיע למשפחות נוספות. זה לוקח פחות מדקה 🙏</p>
    <div class="hero-ctas" style="justify-content:center;margin-top:40px">
      {google_btn}
      <a class="btn {'btn-line' if GOOGLE_REVIEW_URL else 'btn-solid'}" href="{B.WA}?text={B.urlq(msg)}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>שליחת המלצה בוואטסאפ</a>
    </div>
    <p style="margin-top:34px;color:var(--dim);font-size:15px">ליאור ממו · חזן, פייטן ונגן עוד · {B.PHONE}</p>
  </div>
</section>
</main>

{B.TAIL}
<script src="/js/site.js" defer></script>
</body>
</html>
'''
    os.makedirs(os.path.join(B.ROOT, "review"), exist_ok=True)
    open(os.path.join(B.ROOT, "review", "index.html"), "w", encoding="utf-8").write(body)

if __name__ == "__main__":
    page(); print("review page built")
