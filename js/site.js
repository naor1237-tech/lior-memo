(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var MEDIA = '/media/', STREAM = location.hostname.endsWith('netlify.app') ? '/v/' : '/media/';
  var V = [
    {id:'showreel', cat:'reel', title:'שואוריל', sub:'רגעים נבחרים מהבמה', dur:'', hide:true},
    {id:'yeled-gadol', pos:'78% 50%', cat:'shul', title:'״ילד גדול״', sub:'עלייה לתורה · בית הכנסת "משכן יצחק", ירושלים', dur:'1:35'},
    {id:'ya-ozel', cat:'music', title:'״יא עוזל פלפלו״', sub:'עוד: ליאור ממו · כינור: דניאל זכאי', dur:'0:48', w:true},
    {id:'hazan-tefillin', cat:'shul', title:'חזנות בעלייה לתורה', sub:'תפילה חגיגית ושירה עם הקהל', dur:'1:31'},
    {id:'shivchei-yerushalayim', cat:'shul', title:'״שבחי ירושלים״', sub:'עלייה לתורה למשפחת כהן, בליווי הרכב נגנים', dur:'0:55', w:true},
    {id:'zman-lisloach', cat:'music', title:'״זה הזמן לסלוח״', sub:'עם האחים ארז, מול חומות ירושלים', dur:'0:23', w:true},
    {id:'miluim', cat:'army', title:'שירה לחיילים', sub:'הופעה ביחידה, בין המשימות', dur:'0:31'},
    {id:'ensemble', cat:'music', title:'ערב מוזיקה מזרחית', sub:'עוד, כינור וכלי הקשה', dur:'0:25', w:true}
  ];
  function byId(id){ for (var i=0;i<V.length;i++) if (V[i].id===id) return V[i]; return null; }

  // gallery (home page)
  var gal = document.getElementById('gal'), visible = V.filter(function(v){return !v.hide});
  if (gal){
    gal.innerHTML = visible.map(function(v){
      return '<button class="item rv'+(v.w?' w':'')+'" data-open="'+v.id+'" data-cat="'+v.cat+'" aria-label="צפייה: '+v.title.replace(/[״"]/g,'')+'">'+
        '<span class="media"><img src="'+MEDIA+v.id+'.jpg" alt="'+v.title.replace(/[״"]/g,'')+' – '+v.sub.replace(/"/g,'')+'" loading="lazy"'+(v.pos?' style="object-position:'+v.pos+'"':'')+'><span class="ring"><svg><use href="#i-play"/></svg></span></span>'+
        '<span class="meta"><span><h3>'+v.title+'</h3><span class="sub">'+v.sub+'</span></span><span class="dur">'+v.dur+'</span></span></button>';
    }).join('');
    document.querySelectorAll('.tab').forEach(function(t){
      t.addEventListener('click', function(){
        document.querySelectorAll('.tab').forEach(function(x){x.setAttribute('aria-selected', x===t)});
        var f = t.dataset.f;
        gal.querySelectorAll('.item').forEach(function(it){ it.hidden = !(f==='all'||it.dataset.cat===f); });
        visible = V.filter(function(v){return !v.hide && (f==='all'||v.cat===f)});
      });
    });
  }

  // lightbox
  var lb = document.getElementById('lb'), vid = document.getElementById('lbVid'), hero = document.getElementById('heroVid'), list = V, cur = 0;
  if (lb){
    var show = function(i){
      cur = (i + list.length) % list.length; var v = list[cur];
      vid.src = STREAM+v.id+'.mp4'; vid.poster = MEDIA+v.id+'.jpg';
      document.getElementById('lbT').textContent = v.title; document.getElementById('lbS').textContent = v.sub;
      var p = vid.play(); if (p && p.catch) p.catch(function(){});
    };
    var open = function(id){
      if (!byId(id)) return;
      list = visible.some(function(v){return v.id===id}) ? visible : V;
      if (hero) hero.pause();
      lb.showModal ? lb.showModal() : lb.setAttribute('open','');
      show(list.findIndex(function(v){return v.id===id}));
      if (window.gtag) gtag('event','video_open',{video:id});
    };
    var close = function(){ vid.pause(); vid.removeAttribute('src'); vid.load(); lb.close ? lb.close() : lb.removeAttribute('open'); };
    document.addEventListener('click', function(e){ var t = e.target.closest('[data-open]'); if (t){ e.preventDefault(); open(t.dataset.open); } });
    document.getElementById('lbX').onclick = close;
    document.getElementById('lbN').onclick = function(){show(cur+1)};
    document.getElementById('lbP').onclick = function(){show(cur-1)};
    lb.addEventListener('click', function(e){ if (e.target===lb || e.target.classList.contains('lb-in')) close(); });
    lb.addEventListener('close', function(){ vid.pause(); if (hero && !reduce) hero.play().catch(function(){}); });
    lb.addEventListener('keydown', function(e){ if (e.key==='ArrowLeft') show(cur+1); if (e.key==='ArrowRight') show(cur-1); });
  }

  // nav
  var nav = document.getElementById('nav');
  function onScroll(){ nav.classList.toggle('scrolled', window.scrollY > 40); }
  window.addEventListener('scroll', onScroll, {passive:true}); onScroll();
  if (reduce && hero){ hero.removeAttribute('autoplay'); hero.pause(); }

  // scroll-linked motion
  var band = document.getElementById('band'), heroBg = document.querySelector('.hero-bg img'),
      frame = document.querySelector('.reel-frame'), port = document.querySelector('.portrait .ph img'), ticking = false;
  function motion(){
    ticking = false; var y = window.scrollY, vh = innerHeight;
    if (heroBg && y < vh*1.2) heroBg.style.transform = 'scale(1.2) translateY('+(y*0.25)+'px)';
    if (frame && y < vh*1.2) frame.style.translate = '0 '+(y*-0.08)+'px';
    if (band){ var r = band.parentElement.getBoundingClientRect(); if (r.bottom > 0 && r.top < vh) band.style.transform = 'translateX('+((vh - r.top)*0.45 - 300)+'px)'; }
    if (port){ var p = port.getBoundingClientRect(); if (p.bottom > 0 && p.top < vh) port.style.transform = 'scale(1.12) translateY('+((p.top + p.height/2 - vh/2)*-0.06)+'px)'; }
  }
  if (!reduce){ window.addEventListener('scroll', function(){ if(!ticking){ ticking = true; requestAnimationFrame(motion); } }, {passive:true}); motion(); }

  // custom cursor + magnetic buttons (fine pointers only)
  if (!reduce && matchMedia('(hover:hover) and (pointer:fine)').matches){
    var c = document.createElement('div'), d = document.createElement('div');
    c.className = 'cur'; c.innerHTML = '<b>צפייה</b>'; d.className = 'cur-dot';
    document.body.append(c, d);
    var mx = -100, my = -100, cx = -100, cy = -100;
    addEventListener('mousemove', function(e){ mx = e.clientX; my = e.clientY; d.style.transform = 'translate3d('+mx+'px,'+my+'px,0)'; }, {passive:true});
    (function loop(){ cx += (mx-cx)*.18; cy += (my-cy)*.18; c.style.transform = 'translate3d('+cx+'px,'+cy+'px,0)'; requestAnimationFrame(loop); })();
    document.addEventListener('mouseover', function(e){
      var vidT = e.target.closest('[data-open],.reel-frame');
      var linkT = !vidT && e.target.closest('a,button,input,select,textarea,summary');
      c.classList.toggle('big', !!vidT); c.classList.toggle('link', !!linkT);
    });
    document.querySelectorAll('.btn,.icon-btn,.fab').forEach(function(b){
      b.addEventListener('mousemove', function(e){ var r = b.getBoundingClientRect(); b.style.translate = ((e.clientX-r.left-r.width/2)*.18)+'px '+((e.clientY-r.top-r.height/2)*.25)+'px'; });
      b.addEventListener('mouseleave', function(){ b.style.translate = ''; });
    });
  }

  // loader + reveal
  var els = document.querySelectorAll('.rv'), ld = document.getElementById('loader');
  function start(){
    if (ld){ ld.classList.add('done'); setTimeout(function(){ld.style.display='none'},1000); }
    if ('IntersectionObserver' in window && !reduce){
      var io = new IntersectionObserver(function(en){ en.forEach(function(x){ if (x.isIntersecting){ x.target.classList.add('in'); io.unobserve(x.target); } }); }, {rootMargin:'0px 0px -10% 0px', threshold:.06});
      els.forEach(function(el,i){ el.style.transitionDelay = (i%3)*110+'ms'; io.observe(el); });
    } else els.forEach(function(el){el.classList.add('in')});
  }
  if (reduce || !ld) start(); else setTimeout(start, 1100);

  // lead form -> WhatsApp
  var form = document.getElementById('leadForm');
  if (form) form.addEventListener('submit', function(e){
    e.preventDefault();
    var f = e.target, name = f.name.value.trim();
    if (!name){ f.name.focus(); f.name.style.borderBottomColor = '#d9705c'; return; }
    var d = f.date.value ? f.date.value.split('-').reverse().join('/') : 'עוד לא נקבע';
    var lines = ['שלום ליאור, הגעתי מהאתר', 'שם: '+name, 'סוג האירוע: '+f.type.value, 'תאריך: '+d];
    if (f.place.value.trim()) lines.push('מיקום: '+f.place.value.trim());
    if (f.msg.value.trim()) lines.push('פרטים: '+f.msg.value.trim());
    window.open('https://wa.me/972506737715?text='+encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
  });
  var yr = document.getElementById('yr'); if (yr) yr.textContent = new Date().getFullYear();
})();
