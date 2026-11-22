/* Interactive oud: Karplus–Strong plucked-string synthesis + maqam scales with quarter tones. */
(function(){
  var root = document.getElementById('oud'); if (!root) return;
  var ctx = null, master = null, cache = {};
  var STRINGS = [ // open courses, low -> high (Arabic tuning)
    {f:65.41, n:'דו'}, {f:87.31, n:'פה'}, {f:110.0, n:'לה'}, {f:146.83, n:'רה'}, {f:196.0, n:'סול'}, {f:261.63, n:'דו'}
  ];
  var MAQAM = {
    rast:     {name:'ראסט',    base:130.81, c:[0,200,350,500,700,900,1050,1200], n:['דו','רה','מי ½♭','פה','סול','לה','סי ½♭','דו'], mood:'מלכותי ושמח – ״מלך המקאמים״, פותח תפילות ושמחות.'},
    bayati:   {name:'ביאתי',   base:146.83, c:[0,150,300,500,700,800,1000,1200], n:['רה','מי ½♭','פה','סול','לה','סי ♭','דו','רה'], mood:'חם, עממי ומלא רגש – מהמקאמים הנפוצים בפיוט.'},
    hijaz:    {name:'חיג׳אז',  base:146.83, c:[0,100,400,500,700,800,1000,1200], n:['רה','מי ♭','פה ♯','סול','לה','סי ♭','דו','רה'], mood:'הצליל ה״מזרחי״ המוכר – געגוע, מסתורין והתרגשות.'},
    saba:     {name:'סבא',     base:146.83, c:[0,150,300,400,700,800,1000,1200], n:['רה','מי ½♭','פה','סול ♭','לה','סי ♭','דו','רה'], mood:'עצוב ונוגע ללב – מקאם של תחנונים וכיסופים.'},
    nahawand: {name:'נהוונד',  base:130.81, c:[0,200,300,500,700,800,1100,1200], n:['דו','רה','מי ♭','פה','סול','לה ♭','סי','דו'], mood:'רומנטי ומלנכולי – קרוב למינור המערבי.'}
  };
  var cur = 'rast';

  function audio(){
    if (ctx) { if (ctx.state === 'suspended') ctx.resume(); return ctx; }
    var AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null;
    ctx = new AC();
    master = ctx.createGain(); master.gain.value = 0.9;
    // wooden body resonances
    var b1 = ctx.createBiquadFilter(); b1.type = 'peaking'; b1.frequency.value = 220; b1.Q.value = 1.2; b1.gain.value = 5;
    var b2 = ctx.createBiquadFilter(); b2.type = 'peaking'; b2.frequency.value = 1400; b2.Q.value = 1.5; b2.gain.value = 3;
    var lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 5200;
    var comp = ctx.createDynamicsCompressor(); comp.threshold.value = -14; comp.ratio.value = 3;
    // small room reverb
    var conv = ctx.createConvolver(), len = ctx.sampleRate * 1.6, ir = ctx.createBuffer(2, len, ctx.sampleRate);
    for (var ch = 0; ch < 2; ch++){ var d = ir.getChannelData(ch); for (var i = 0; i < len; i++) d[i] = (Math.random()*2-1) * Math.pow(1 - i/len, 3.2); }
    conv.buffer = ir;
    var wet = ctx.createGain(); wet.gain.value = 0.22;
    master.connect(b1); b1.connect(b2); b2.connect(lp); lp.connect(comp);
    lp.connect(conv); conv.connect(wet); wet.connect(comp);
    comp.connect(ctx.destination);
    return ctx;
  }

  function pluckBuffer(freq){
    var key = Math.round(freq*100); if (cache[key]) return cache[key];
    var sr = ctx.sampleRate, dur = Math.min(4.2, 2.2 + 120/freq), len = Math.floor(sr*dur);
    var buf = ctx.createBuffer(1, len, sr), out = buf.getChannelData(0);
    var N = Math.max(2, Math.round(sr / freq)), ring = new Float32Array(N);
    // excitation: noise shaped by pluck position (risha near the bridge = bright, nasal)
    var pos = Math.max(1, Math.round(N * 0.13)), prev = 0;
    for (var i = 0; i < N; i++){ var r = Math.random()*2-1; prev = prev*0.35 + r*0.65; ring[i] = prev; }
    for (i = N-1; i >= pos; i--) ring[i] -= ring[i-pos];
    var decay = 0.9965 + Math.min(0.003, freq/250000), idx = 0, last = 0, s = 0;
    for (i = 0; i < len; i++){
      var a = ring[idx], nx = ring[(idx+1) % N];
      s = decay * (0.5*(a + nx));
      // slight brightness-preserving blend for the nasal oud tone
      ring[idx] = s*0.985 + (a - last)*0.015; last = a;
      out[i] = a;
      idx = (idx+1) % N;
    }
    // risha attack click + fades
    for (i = 0; i < Math.min(len, 220); i++) out[i] += (Math.random()*2-1) * 0.25 * (1 - i/220);
    var peak = 0; for (i = 0; i < len; i++) peak = Math.max(peak, Math.abs(out[i]));
    var g = 0.55 / (peak || 1), fade = Math.floor(sr*0.25);
    for (i = 0; i < len; i++){ out[i] *= g; if (i > len - fade) out[i] *= (len - i)/fade; }
    return cache[key] = buf;
  }

  function play(freq, when, vel){
    if (!audio()) return;
    var src = ctx.createBufferSource(); src.buffer = pluckBuffer(freq);
    var g = ctx.createGain(); g.gain.value = vel || 0.9;
    var pan = ctx.createStereoPanner ? ctx.createStereoPanner() : null;
    src.connect(g); if (pan){ pan.pan.value = (Math.random()-.5)*0.3; g.connect(pan); pan.connect(master); } else g.connect(master);
    src.start(when || ctx.currentTime);
  }

  // ---------- strings (strum panel + illustration) ----------
  var panel = root.querySelector('.strum'), btns = [].slice.call(root.querySelectorAll('.strum .s')).reverse(), svgStr = [].slice.call(root.querySelectorAll('.oud-svg .str'));
  function vibrate(i){
    [btns[i], svgStr[i]].forEach(function(el){ if (!el) return; el.classList.remove('vib'); void el.getBoundingClientRect(); el.classList.add('vib'); });
  }
  function pluckString(i, vel){ play(STRINGS[i].f, 0, vel); vibrate(i); }
  btns.forEach(function(b, i){ b.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); pluckString(i); } }); });

  var down = false, lastIdx = -1;
  function idxAt(y){
    for (var i = 0; i < btns.length; i++){ var r = btns[i].getBoundingClientRect(); if (y >= r.top && y <= r.bottom) return i; }
    return -1;
  }
  panel.addEventListener('pointerdown', function(e){ down = true; audio(); panel.setPointerCapture && panel.setPointerCapture(e.pointerId); var i = idxAt(e.clientY); if (i > -1){ pluckString(i); lastIdx = i; } });
  panel.addEventListener('pointermove', function(e){
    if (!down) return; var i = idxAt(e.clientY);
    if (i > -1 && i !== lastIdx){
      // fill skipped strings when strumming fast
      if (lastIdx > -1){ var step = i > lastIdx ? 1 : -1; for (var k = lastIdx + step; k !== i; k += step) pluckString(k, 0.7); }
      pluckString(i, 0.8); lastIdx = i;
    }
  });
  ['pointerup','pointercancel','pointerleave'].forEach(function(t){ panel.addEventListener(t, function(){ down = false; lastIdx = -1; }); });

  // ---------- maqam pads ----------
  var padsEl = root.querySelector('.pads'), moodEl = root.querySelector('.mood'), tabs = [].slice.call(root.querySelectorAll('.mq'));
  function freqOf(m, i){ return m.base * Math.pow(2, m.c[i]/1200); }
  function renderPads(){
    var m = MAQAM[cur];
    padsEl.innerHTML = m.n.map(function(n, i){ return '<button type="button" class="pad" data-i="'+i+'"><b>'+n+'</b><small>'+(i+1)+'</small></button>'; }).join('');
    moodEl.innerHTML = '<b>מקאם '+m.name+'</b> – '+m.mood;
  }
  function hit(i, when){
    var m = MAQAM[cur], p = padsEl.children[i];
    play(freqOf(m, i), when);
    if (!p) return;
    var delay = when && ctx ? Math.max(0, (when - ctx.currentTime)*1000) : 0;
    setTimeout(function(){ p.classList.remove('on'); void p.offsetWidth; p.classList.add('on'); svgStr.length && vibrate(Math.min(5, 2 + (i>>1))); }, delay);
  }
  padsEl.addEventListener('pointerdown', function(e){ var p = e.target.closest('.pad'); if (p){ e.preventDefault(); hit(+p.dataset.i); } });
  tabs.forEach(function(t){ t.addEventListener('click', function(){ tabs.forEach(function(x){ x.setAttribute('aria-pressed', x === t); }); cur = t.dataset.m; renderPads(); }); });
  root.addEventListener('keydown', function(e){ var k = +e.key; if (k >= 1 && k <= 8 && !e.target.matches('input,textarea')){ hit(k-1); } });

  // short taqsim-like phrase
  var PHRASE = [[0,.0],[1,.28],[2,.5],[3,.72],[4,1.1],[3,1.5],[4,1.68],[5,1.86],[4,2.3],[2,2.6],[3,2.78],[1,3.1],[2,3.3],[0,3.7],[4,4.3],[7,4.75],[6,5.1],[5,5.3],[4,5.5],[3,5.9],[2,6.1],[1,6.3],[0,6.8]];
  var playing = false;
  root.querySelector('.taqsim').addEventListener('click', function(){
    if (!audio() || playing) return; playing = true;
    var t0 = ctx.currentTime + 0.08;
    PHRASE.forEach(function(p){ hit(p[0], t0 + p[1]); if (p[1] === 0 || p[1] === 4.3) setTimeout(function(){ play(freqOf(MAQAM[cur],0)/2, ctx.currentTime, .6); }, p[1]*1000); });
    setTimeout(function(){ playing = false; }, 7600);
  });
  renderPads();
})();
