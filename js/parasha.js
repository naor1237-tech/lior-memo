(function(){
  var form = document.getElementById('calc'), res = document.getElementById('res');
  if (!form) return;
  var API = 'https://www.hebcal.com/';
  var HE_MONTHS = ['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר'];
  var DAYS = ['ראשון','שני','שלישי','רביעי','חמישי','שישי','שבת'];
  function isLeap(y){ return ((7*y + 1) % 19) < 7; }
  function noNiqqud(s){ return (s||'').replace(/[֑-ׇ]/g,''); }
  function pad(n){ return (n<10?'0':'')+n; }
  function iso(d){ return d.getUTCFullYear()+'-'+pad(d.getUTCMonth()+1)+'-'+pad(d.getUTCDate()); }
  function gfmt(d){ return 'יום '+DAYS[d.getUTCDay()]+', '+d.getUTCDate()+' ב'+HE_MONTHS[d.getUTCMonth()]+' '+d.getUTCFullYear(); }
  function get(url){ return fetch(url).then(function(r){ if(!r.ok) throw new Error('net'); return r.json(); }); }
  var BOOKS = {'Genesis':'בראשית','Exodus':'שמות','Leviticus':'ויקרא','Numbers':'במדבר','Deuteronomy':'דברים','Joshua':'יהושע','Judges':'שופטים',
    'I Samuel':'שמואל א','II Samuel':'שמואל ב','I Kings':'מלכים א','II Kings':'מלכים ב','Isaiah':'ישעיהו','Jeremiah':'ירמיהו','Ezekiel':'יחזקאל',
    'Hosea':'הושע','Joel':'יואל','Amos':'עמוס','Obadiah':'עובדיה','Jonah':'יונה','Micah':'מיכה','Nahum':'נחום','Habakkuk':'חבקוק','Zephaniah':'צפניה',
    'Haggai':'חגי','Zechariah':'זכריה','Malachi':'מלאכי','Esther':'אסתר','Ruth':'רות','Song of Songs':'שיר השירים','Ecclesiastes':'קהלת','Lamentations':'איכה'};
  function gem(n){ n=+n; if(!n) return ''; var o='', v=[[400,'ת'],[300,'ש'],[200,'ר'],[100,'ק'],[90,'צ'],[80,'פ'],[70,'ע'],[60,'ס'],[50,'נ'],[40,'מ'],[30,'ל'],[20,'כ'],[10,'י'],[9,'ט'],[8,'ח'],[7,'ז'],[6,'ו'],[5,'ה'],[4,'ד'],[3,'ג'],[2,'ב'],[1,'א']];
    while(n>0){ if(n===15){o+='טו';break;} if(n===16){o+='טז';break;} for(var i=0;i<v.length;i++){ if(n>=v[i][0]){ o+=v[i][1]; n-=v[i][0]; break; } } } return o; }
  function cv(x){ var p=String(x).split(':'); return gem(p[0])+(p[1]?' '+gem(p[1]):''); }
  function heRef(r){
    if(!r) return ''; return String(r).split(/;\s*/).map(function(part){
      var m = part.match(/^([A-Za-z ]+?)\s+(\d+:\d+)(?:-(\d+(?::\d+)?))?$/);
      if(!m){ var m2 = part.match(/^(\d+:\d+)(?:-(\d+(?::\d+)?))?$/); if(m2) return cv(m2[1])+(m2[2]?'–'+cv(m2[2]):''); return part; }
      var b = BOOKS[m[1].trim()] || m[1]; return b+' '+cv(m[2])+(m[3]?'–'+cv(m[3]):'');
    }).join('; '); }
  function refObj(o){ return o ? heRef(o.k+' '+o.b+'-'+o.e) : ''; }
  function esc(s){ return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]}); }

  form.addEventListener('submit', function(e){
    e.preventDefault();
    var d = +document.getElementById('cDay').value, m = +document.getElementById('cMonth').value, y = +document.getElementById('cYear').value;
    var sunset = document.getElementById('cSunset').checked, abroad = document.getElementById('cDiaspora').checked;
    var nsEl = document.getElementById('cNusach'), nusach = nsEl ? nsEl.value : 'ספרדי־ירושלמי', ashk = nusach === 'אשכנזי';
    var dt = new Date(Date.UTC(y, m-1, d));
    if (!d || !y || dt.getUTCDate() !== d || y < 1950 || y > 2035){
      res.className = 'result on'; res.innerHTML = '<p class="err">נא להזין תאריך לידה תקין.</p>'; return;
    }
    res.className = 'result on'; res.innerHTML = '<p style="color:var(--muted)">מחשב לפי הלוח העברי…</p>';
    var birth;
    get(API+'converter?cfg=json&g2h=1&gy='+y+'&gm='+m+'&gd='+d+(sunset?'&gs=on':''))
    .then(function(b){
      birth = b;
      var hy = b.hy + 13, hm = b.hm;
      if (hm === 'Adar' && isLeap(hy)) hm = 'Adar II';
      else if ((hm === 'Adar I' || hm === 'Adar II') && !isLeap(hy)) hm = 'Adar';
      return get(API+'converter?cfg=json&h2g=1&hy='+hy+'&hm='+encodeURIComponent(hm)+'&hd='+b.hd);
    })
    .then(function(bm){
      var bmDate = new Date(Date.UTC(bm.gy, bm.gm-1, bm.gd));
      var shabbat = new Date(bmDate.getTime() + ((6 - bmDate.getUTCDay() + 7) % 7) * 864e5);
      return get(API+'leyning?cfg=json&start='+iso(shabbat)+'&end='+iso(shabbat)+'&i='+(abroad?'off':'on'))
        .then(function(l){ return {bm:bm, bmDate:bmDate, shabbat:shabbat, ley:l}; });
    })
    .then(function(o){
      var item = (o.ley.items||[])[0] || {};
      var name = noNiqqud(item.name && item.name.he) || '—';
      var title = item.type === 'shabbat' ? 'פרשת ' + name : name;
      res.innerHTML =
        '<span class="label">הפרשה של הבר מצווה</span>'+
        '<div class="big">'+esc(title)+'</div>'+
        '<dl>'+
          '<div><dt>תאריך לידה עברי</dt><dd>'+esc(noNiqqud(birth.hebrew))+'</dd></div>'+
          '<div><dt>יום הבר מצווה</dt><dd>'+esc(noNiqqud(o.bm.hebrew))+'<br><span style="color:var(--muted);font-size:16px">'+gfmt(o.bmDate)+'</span></dd></div>'+
          '<div><dt>שבת העלייה לתורה</dt><dd>'+gfmt(o.shabbat)+'</dd></div>'+
          (item.summary ? '<div><dt>קריאת התורה</dt><dd>'+esc(heRef(item.summary))+'</dd></div>' : '')+
          (item.fullkriyah && item.fullkriyah.M ? '<div><dt>מפטיר</dt><dd>'+esc(refObj(item.fullkriyah.M))+'</dd></div>' : '')+
          ((ashk ? item.haftara : (item.sephardic || item.haftara)) ? '<div><dt>הפטרה · '+(ashk?'נוסח אשכנז':'נוסח ספרד ועדות המזרח')+'</dt><dd>'+esc(heRef(ashk ? item.haftara : (item.sephardic || item.haftara)))+'</dd></div>' : '')+
        '</dl>'+
        '<div class="note-prep"><b>הכנה מדויקת בטעמים – נוסח '+esc(nusach)+'</b>ליאור מלווה את הבר מצווה בלימוד הפרשה, המפטיר וההפטרה מילה במילה ובטעמי המקרא לפי מסורת המשפחה – ועד העלייה לתורה, גם בליווי נגנים.</div>'+
        '<p style="color:var(--muted);font-size:15px;margin-top:18px">החישוב '+(abroad?'לחוץ לארץ':'לישראל')+'. במקרים מיוחדים (אדר בשנה מעוברת, ל׳ בחשוון/כסלו) מומלץ לאמת עם רב הקהילה.</p>'+
        '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:22px">'+
          '<a class="btn btn-solid" target="_blank" rel="noopener" href="https://wa.me/972506737715?text='+encodeURIComponent('שלום ליאור, הבר מצווה של הבן שלנו בפרשת '+name+' ('+o.shabbat.getUTCDate()+'/'+(o.shabbat.getUTCMonth()+1)+'/'+o.shabbat.getUTCFullYear()+'), נוסח טעמים: '+nusach+'. נשמח לשמוע על לימוד הפרשה והכנה לבר מצווה, ועל ליווי בעלייה לתורה (גם עם נגנים)')+'">לתיאום לימוד הפרשה עם ליאור</a>'+
          '<a class="btn btn-line" href="/hachana-bar-mitzvah/">על ההכנה לבר מצווה</a>'+
        '</div>';
      if (item.name && item.name.en){
        fetch('/js/parashot-map.json').then(function(r){ return r.json(); }).then(function(map){
          var en = item.name.en, sl = map[en] || (en.indexOf('-') > 0 ? map[en.split('-')[0]] : null);
          if (!sl) return;
          var a = document.createElement('a'); a.className = 'btn btn-line'; a.href = '/parasha/' + sl + '/';
          a.textContent = 'לעמוד הפרשה: עליות, מפטיר והפטרה בטעמים';
          var row = res.querySelector('div[style*="flex"]'); if (row) row.appendChild(a);
        }).catch(function(){});
      }
      if (window.gtag) gtag('event','parasha_calc',{parasha:name});
    })
    .catch(function(){
      res.innerHTML = '<p class="err">לא הצלחנו להתחבר ללוח השנה העברי. נסו שוב בעוד רגע.</p>';
    });
  });
})();
