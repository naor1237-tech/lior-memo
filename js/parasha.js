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
  function esc(s){ return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]}); }

  form.addEventListener('submit', function(e){
    e.preventDefault();
    var d = +document.getElementById('cDay').value, m = +document.getElementById('cMonth').value, y = +document.getElementById('cYear').value;
    var sunset = document.getElementById('cSunset').checked, abroad = document.getElementById('cDiaspora').checked;
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
        '</dl>'+
        '<p style="color:var(--muted);font-size:15px;margin-top:18px">החישוב '+(abroad?'לחוץ לארץ':'לישראל')+'. במקרים מיוחדים (אדר בשנה מעוברת, ל׳ בחשוון/כסלו) מומלץ לאמת עם רב הקהילה.</p>'+
        '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:22px">'+
          '<a class="btn btn-solid" target="_blank" rel="noopener" href="https://wa.me/972506737715?text='+encodeURIComponent('שלום ליאור, הבר מצווה של הבן שלנו בפרשת '+name+' ('+o.shabbat.getUTCDate()+'/'+(o.shabbat.getUTCMonth()+1)+'/'+o.shabbat.getUTCFullYear()+'). נשמח לשמוע על הכנה לבר מצווה ועלייה לתורה')+'">לתיאום הכנה ועלייה לתורה</a>'+
          '<a class="btn btn-line" href="/hachana-bar-mitzvah/">על ההכנה לבר מצווה</a>'+
        '</div>';
      if (window.gtag) gtag('event','parasha_calc',{parasha:name});
    })
    .catch(function(){
      res.innerHTML = '<p class="err">לא הצלחנו להתחבר ללוח השנה העברי. נסו שוב בעוד רגע.</p>';
    });
  });
})();
