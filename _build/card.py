# -*- coding: utf-8 -*-
"""Digital business card: /card/ (+ /c short link) and a downloadable vCard /lior-mamo.vcf."""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

CARD_URL = B.SITE + "/card/"

def vcard():
    photo = ""
    pth = os.path.join(B.ROOT, "media", "card-photo.jpg")
    if os.path.exists(pth):
        b64 = base64.b64encode(open(pth, "rb").read()).decode()
        photo = "PHOTO;ENCODING=b;TYPE=JPEG:" + "\r\n ".join(b64[i:i+74] for i in range(0, len(b64), 74)) + "\r\n"
    v = ("BEGIN:VCARD\r\nVERSION:3.0\r\nN:ממו;ליאור;;;\r\nFN:ליאור ממו\r\nORG:ליאור ממו – חזן ופייטן\r\n"
         "TITLE:חזן\\, פייטן\\, בעל קורא ונגן עוד\r\nTEL;TYPE=CELL,VOICE:+972506737715\r\n"
         f"URL:{B.SITE}/\r\nURL;TYPE=WhatsApp:https://wa.me/972506737715\r\n"
         "ADR;TYPE=WORK:;;;ירושלים;;;ישראל\r\n"
         "NOTE:ליווי והכנה לבר מצווה\\, עליות לתורה\\, שבת חתן\\, פיוטים ונגן עוד לאירועים.\r\n"
         + photo + "END:VCARD\r\n")
    open(os.path.join(B.ROOT, "lior-mamo.vcf"), "w", encoding="utf-8", newline="").write(v)

def page():
    wa = B.WA + "?text=" + B.urlq("שלום ליאור, הגעתי מכרטיס הביקור שלך")
    share_txt = "ליאור ממו – חזן, פייטן, בעל קורא ונגן עוד 🎶\nכרטיס ביקור: " + CARD_URL
    body = B.head("ליאור ממו – כרטיס ביקור דיגיטלי", "כרטיס ביקור דיגיטלי של ליאור ממו – חזן, פייטן, בעל קורא ונגן עוד. חיוג, וואטסאפ, שמירת איש קשר ועוד.", "/card/",
                  {"@context":"https://schema.org","@type":"ProfilePage","mainEntity":{"@id":B.BUSINESS_ID}}, image="card-photo.jpg") \
        .replace('<meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1">', '<meta name="robots" content="noindex,follow">') \
        .replace('<link rel="stylesheet" href="/css/site.css">', '<link rel="stylesheet" href="/css/site.css">\n<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcode-generator/1.4.4/qrcode.min.js" defer></script>')
    body += B.sprite() + f'''
<main class="dcard">
  <div class="dc-bg" aria-hidden="true"><img src="/media/lior-oud.jpg" alt=""></div>
  <section class="dc">
    <div class="dc-photo"><img src="/media/card-photo.jpg" alt="ליאור ממו מנגן בעוד"></div>
    <h1>ליאור ממו</h1>
    <p class="dc-role">חזן · פייטן · בעל קורא · נגן עוד</p>
    <p class="dc-tag">ליווי והכנה לבר מצווה · עליות לתורה · שבת חתן · אירועים</p>

    <div class="dc-main">
      <a class="dc-btn gold" href="tel:+972506737715"><svg><use href="#i-phone"/></svg><span>חיוג</span></a>
      <a class="dc-btn green" href="{wa}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg><span>וואטסאפ</span></a>
      <a class="dc-btn" href="/lior-mamo.vcf" download="ליאור-ממו.vcf"><svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8M19 8v6M22 11h-6"/></svg><span>שמירת איש קשר</span></a>
    </div>

    <nav class="dc-list" aria-label="קישורים">
      <a href="/?utm_source=card"><b>🌐</b>האתר המלא<i>←</i></a>
      <a href="#" data-open="showreel"><b>🎬</b>שואוריל – רגעים מהבמה<i>←</i></a>
      <a href="/hachana-bar-mitzvah/?utm_source=card"><b>📖</b>ליווי והכנה לבר מצווה<i>←</i></a>
      <a href="/parasha/?utm_source=card"><b>🗓️</b>מה הפרשה של הבן שלי?<i>←</i></a>
      <a href="/bar-mitzvah/?utm_source=card"><b>🕍</b>עלייה לתורה עם נגנים<i>←</i></a>
      <a href="/nagan-oud/?utm_source=card"><b>🪕</b>נגן עוד – נסו לנגן<i>←</i></a>
      <a href="/r"><b>⭐</b>כתבו לי ביקורת<i>←</i></a>
    </nav>

    <div class="dc-foot">
      <button type="button" class="dc-mini" id="dcShare">שיתוף הכרטיס</button>
      <button type="button" class="dc-mini" id="dcQr">QR להצגה</button>
    </div>
    <div class="dc-qr" id="dcQrBox" hidden><div id="dcQrCode"></div><p>סרקו כדי לשמור את הכרטיס</p></div>
    <p class="dc-num" dir="ltr">050-6737715</p>
  </section>
</main>

{B.TAIL}
<script src="/js/site.js" defer></script>
<script>
document.addEventListener('DOMContentLoaded',function(){{
  var url = '{CARD_URL}';
  document.getElementById('dcShare').onclick = function(){{
    if (navigator.share) navigator.share({{title:'ליאור ממו – כרטיס ביקור', text:'ליאור ממו – חזן, פייטן, בעל קורא ונגן עוד', url:url}}).catch(function(){{}});
    else window.open('https://wa.me/?text={B.urlq(share_txt)}','_blank','noopener');
  }};
  document.getElementById('dcQr').onclick = function(){{
    var box = document.getElementById('dcQrBox'), c = document.getElementById('dcQrCode');
    if (!c.innerHTML && window.qrcode){{ var q = qrcode(0,'M'); q.addData(url+'?utm_source=qr'); q.make(); c.innerHTML = q.createSvgTag({{cellSize:5,margin:0,scalable:true}}); }}
    box.hidden = !box.hidden;
  }};
}});
</script>
</body>
</html>
'''
    os.makedirs(os.path.join(B.ROOT, "card"), exist_ok=True)
    open(os.path.join(B.ROOT, "card", "index.html"), "w", encoding="utf-8").write(body)

if __name__ == "__main__":
    vcard(); page(); print("card built")
