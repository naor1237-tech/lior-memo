/* Weekly Shabbat bar (home) + daily zmanim board (/zmanim/) – live from Hebcal, city selectable. */
(function(){
  var CITIES = [['281184','ירושלים',40],['293397','תל אביב',20],['294801','חיפה',30],['295530','באר שבע',20],['295432','בית שמש',20],['282926','מודיעין',20],['295514','בני ברק',20],['293100','צפת',20]];
  var city = '281184';
  try { city = localStorage.getItem('zmCity') || city; } catch(e){}
  var C = function(){ for (var i=0;i<CITIES.length;i++) if (CITIES[i][0]===city) return CITIES[i]; return CITIES[0]; };
  var TZ = 'Asia/Jerusalem';
  function hm(t){ return t ? new Intl.DateTimeFormat('he-IL',{timeZone:TZ,hour:'2-digit',minute:'2-digit',hour12:false}).format(new Date(t)) : '—'; }
  function ymd(d){ var p = new Intl.DateTimeFormat('en-CA',{timeZone:TZ,year:'numeric',month:'2-digit',day:'2-digit'}).format(d); return p; }
  function get(u){ return fetch(u).then(function(r){ if(!r.ok) throw 0; return r.json(); }); }
  function noNiq(s){ return (s||'').replace(/[֑-ׇ]/g,''); }
  function slug(en){ return (en||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,''); }
  function cityPicker(el, onChange){
    if (!el) return;
    el.innerHTML = CITIES.map(function(c){ return '<option value="'+c[0]+'"'+(c[0]===city?' selected':'')+'>'+c[1]+'</option>'; }).join('');
    el.addEventListener('change', function(){ city = el.value; try{ localStorage.setItem('zmCity', city); }catch(e){} onChange(); });
  }

  // ---------- weekly Shabbat (home + zmanim page) ----------
  function shabbat(box){
    if (!box) return;
    var c = C();
    get('https://www.hebcal.com/shabbat?cfg=json&geonameid='+c[0]+'&b='+c[2]+'&M=on&lg=he').then(function(d){
      var it = d.items || [], cand = it.find(function(i){return i.category==='candles';}), hav = it.find(function(i){return i.category==='havdalah';}),
          par = it.find(function(i){return i.category==='parashat';});
      var en = par ? (par.title_orig || '').replace(/^Parashat /,'') : '';
      var pl = par ? '<a href="/parasha/'+slug(en.split('-')[0])+'/">'+noNiq(par.hebrew || par.title)+'</a>' : '—';
      box.querySelector('[data-z=par]').innerHTML = pl;
      box.querySelector('[data-z=in]').textContent = hm(cand && cand.date);
      box.querySelector('[data-z=out]').textContent = hm(hav && hav.date);
      var cn = box.querySelector('[data-z=city]'); if (cn) cn.textContent = c[1];
      box.classList.add('ready');
    }).catch(function(){ box.classList.add('err'); });
  }

  // ---------- daily zmanim board ----------
  var LIST = [['alotHaShachar','עלות השחר'],['misheyakir','משיכיר (זמן טלית ותפילין)'],['sunrise','הנץ החמה (זריחה)'],['sofZmanShmaMGA','סוף זמן ק״ש – מג״א'],['sofZmanShma','סוף זמן ק״ש – גר״א'],
              ['sofZmanTfilla','סוף זמן תפילה – גר״א'],['chatzot','חצות היום'],['minchaGedola','מנחה גדולה'],['minchaKetana','מנחה קטנה'],['plagHaMincha','פלג המנחה'],
              ['sunset','שקיעה'],['tzeit7083deg','צאת הכוכבים'],['chatzotNight','חצות הלילה']];
  var timer;
  function board(box){
    if (!box) return;
    var c = C(), today = ymd(new Date());
    Promise.all([get('https://www.hebcal.com/zmanim?cfg=json&geonameid='+c[0]+'&date='+today),
                 get('https://www.hebcal.com/converter?cfg=json&date='+today+'&g2h=1&strict=1')]).then(function(r){
      var t = r[0].times || {}, h = r[1];
      box.querySelector('[data-z=hdate]').textContent = noNiq(h.hebrew || '');
      box.querySelector('[data-z=gdate]').textContent = new Intl.DateTimeFormat('he-IL',{timeZone:TZ,weekday:'long',day:'numeric',month:'long',year:'numeric'}).format(new Date());
      box.querySelector('[data-z=list]').innerHTML = LIST.map(function(z){ return '<li data-t="'+(t[z[0]]?Date.parse(t[z[0]]):'')+'"><span>'+z[1]+'</span><b>'+hm(t[z[0]])+'</b></li>'; }).join('');
      tick(box); clearInterval(timer); timer = setInterval(function(){ tick(box); }, 1000);
      box.classList.add('ready');
    }).catch(function(){ box.classList.add('err'); });
  }
  function tick(box){
    var now = Date.now(), clock = box.querySelector('[data-z=clock]');
    if (clock) clock.textContent = new Intl.DateTimeFormat('he-IL',{timeZone:TZ,hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false}).format(new Date());
    var lis = box.querySelectorAll('[data-z=list] li'), next = null;
    lis.forEach(function(li){ var t = +li.dataset.t; li.classList.toggle('past', t && t < now); li.classList.remove('next'); if (!next && t > now) next = li; });
    if (next){ next.classList.add('next'); var s = Math.round((+next.dataset.t - now)/1000), hh=Math.floor(s/3600), mm=Math.floor(s%3600/60), ss=s%60;
      var nx = box.querySelector('[data-z=next]'); if (nx) nx.innerHTML = 'הזמן הבא: <b>'+next.querySelector('span').textContent+'</b> בעוד '+(hh?hh+':':'')+String(mm).padStart(2,'0')+':'+String(ss).padStart(2,'0'); }
  }

  // home bar: Friday (and Shabbat) show candle lighting/havdalah, other days show today's key zmanim
  function weekBar(box){
    if (!box) return;
    var wd = new Intl.DateTimeFormat('en-US',{timeZone:TZ,weekday:'short'}).format(new Date());
    var fri = (wd === 'Fri' || wd === 'Sat');
    box.classList.toggle('is-fri', fri);
    if (fri) return;
    var c = C();
    get('https://www.hebcal.com/zmanim?cfg=json&geonameid='+c[0]+'&date='+ymd(new Date())).then(function(d){
      var t = d.times || {};
      box.querySelector('[data-z=sunrise]').textContent = hm(t.sunrise);
      box.querySelector('[data-z=shma]').textContent = hm(t.sofZmanShma);
      box.querySelector('[data-z=sunset]').textContent = hm(t.sunset);
      var c2 = box.querySelector('[data-z=city2]'); if (c2) c2.textContent = c[1];
    }).catch(function(){});
  }
  var sb = document.getElementById('shabbatBar'), zb = document.getElementById('zmanimBoard'), zs = document.getElementById('zmanimShabbat');
  shabbat(sb); weekBar(sb); shabbat(zs); board(zb);
  document.querySelectorAll('[data-z=picker]').forEach(function(el){ cityPicker(el, function(){ shabbat(sb); shabbat(zs); board(zb); document.querySelectorAll('[data-z=picker]').forEach(function(o){ o.value = city; }); }); });
})();
