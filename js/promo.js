/* Context-aware promo bar: appears after the visitor scrolls, matched to the page they came for. Dismissible per session. */
(function(){
  var p = location.pathname, WA = 'https://wa.me/972506737715?text=';
  var RULES = [
    [/^\/tefilot\//, '🎶', 'חוגגים שמחה? ליאור ממו – חזן ופייטן לבר מצווה ושבת חתן', '/bar-mitzvah/', 'לפרטים', 'שלום ליאור, הגעתי מדף התפילות באתר ואשמח לפרטים על אירוע'],
    [/^\/parasha\//, '📖', 'לימוד הפרשה בטעמים – הכנה מדויקת לבר מצווה עם ליאור', '/hachana-bar-mitzvah/', 'לפרטים', 'שלום ליאור, הגעתי ממחשבון הפרשה ואשמח לשמוע על הכנה לבר מצווה'],
    [/^\/nagan-oud\//, '🪕', 'רוצים ללמוד לנגן על עוד? שיעורים פרטיים עם ליאור', '/shiurei-oud/', 'לשיעורים', 'שלום ליאור, אשמח לשמוע על שיעורים פרטיים בעוד'],
    [/^\/shiurei-oud\//, '🎶', 'צריכים נגן עוד לאירוע? ליאור מנגן גם בשמחות', '/nagan-oud/', 'לפרטים', 'שלום ליאור, אשמח לפרטים על נגינה בעוד באירוע'],
    [/^\/(bar-mitzvah|hachana-bar-mitzvah)\//, '🗓️', 'מה הפרשה של הבן שלכם? מחשבון חינמי לפי נוסח הטעמים', '/parasha/', 'למחשבון', 'שלום ליאור, אשמח לפרטים על בר מצווה'],
    [/^\/shabbat-chatan\//, '💍', 'גם בשבע ברכות – פיוטים, זמר ועוד בליווי ליאור ממו', '/shabbat-chatan/#top', 'לפרטים', 'שלום ליאור, אשמח לפרטים על שבת חתן ושבע ברכות']
  ];
  var r = null;
  for (var i = 0; i < RULES.length; i++) if (RULES[i][0].test(p)) { r = RULES[i]; break; }
  if (!r) return;
  try { if (sessionStorage.getItem('pbarClosed') === p) return; } catch(e){}
  var bar = document.createElement('aside');
  bar.className = 'pbar'; bar.setAttribute('aria-label', 'הצעה מליאור ממו');
  bar.innerHTML = '<span class="pbar-i" aria-hidden="true">' + r[1] + '</span><p>' + r[2] + '</p>' +
    '<a class="pbar-go" href="' + r[3] + '">' + r[4] + '</a>' +
    '<a class="pbar-wa" href="' + WA + encodeURIComponent(r[5]) + '" target="_blank" rel="noopener" aria-label="וואטסאפ לליאור"><svg><use href="#i-wa"/></svg></a>' +
    '<button type="button" class="pbar-x" aria-label="סגירת ההצעה">✕</button>';
  document.body.appendChild(bar);
  var shown = false;
  function check(){
    var h = document.documentElement.scrollHeight - innerHeight;
    var on = h > 0 && scrollY / h > 0.22;
    if (on !== shown){ shown = on; bar.classList.toggle('on', on); document.body.classList.toggle('pbar-on', on); }
  }
  addEventListener('scroll', check, {passive:true}); check();
  bar.querySelector('.pbar-x').addEventListener('click', function(){
    bar.remove(); document.body.classList.remove('pbar-on'); removeEventListener('scroll', check);
    try { sessionStorage.setItem('pbarClosed', p); } catch(e){}
  });
})();
