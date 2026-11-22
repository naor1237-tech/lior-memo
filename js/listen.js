/* In-site listening for parasha pages: chanted recordings (PocketTorah, CC BY-SA) in a mini player,
   plus "read aloud" of the maftir/haftarah text with the device's Hebrew voice (Web Speech API). */
(function(){
  var btns = document.querySelectorAll('[data-audio]'); if (!btns.length && !document.querySelector('[data-tts]')) return;
  var bar = document.createElement('div'); bar.className = 'lplayer'; bar.hidden = true; bar.setAttribute('role','region'); bar.setAttribute('aria-label','נגן האזנה');
  bar.innerHTML = '<button type="button" class="lp-pp" aria-label="ניגון/השהיה">❚❚</button><div class="lp-mid"><b class="lp-t"></b><input type="range" class="lp-r" min="0" max="100" value="0" step="0.1" aria-label="מיקום בהקלטה"><small class="lp-time">0:00</small></div>' +
    '<button type="button" class="lp-sp" aria-label="מהירות">1×</button><button type="button" class="lp-x" aria-label="סגירת הנגן">✕</button>';
  document.body.appendChild(bar);
  var au = new Audio(); au.preload = 'none';
  var t = bar.querySelector('.lp-t'), pp = bar.querySelector('.lp-pp'), r = bar.querySelector('.lp-r'), tm = bar.querySelector('.lp-time'), sp = bar.querySelector('.lp-sp');
  var speeds = [1, 0.75, 0.5], si = 0, current = null;
  function f(s){ s = Math.floor(s || 0); return Math.floor(s/60) + ':' + String(s%60).padStart(2,'0'); }
  function mark(b){ btns.forEach(function(x){ x.classList.toggle('on', x === b); x.textContent = x === b && !au.paused ? '❚❚ מתנגן' : '▶ האזנה'; }); }
  btns.forEach(function(b){
    b.addEventListener('click', function(){
      stopTTS();
      if (current === b && !au.paused){ au.pause(); return; }
      if (current !== b){ au.src = b.dataset.audio; current = b; t.textContent = b.dataset.label || 'האזנה'; }
      bar.hidden = false; document.body.classList.add('lp-on');
      au.play().catch(function(){});
    });
  });
  au.addEventListener('play', function(){ pp.textContent = '❚❚'; mark(current); });
  au.addEventListener('pause', function(){ pp.textContent = '▶'; mark(current); });
  au.addEventListener('timeupdate', function(){ if (au.duration){ r.value = au.currentTime / au.duration * 100; tm.textContent = f(au.currentTime) + ' / ' + f(au.duration); } });
  au.addEventListener('ended', function(){ var arr = [].slice.call(btns), i = arr.indexOf(current); if (i > -1 && i + 1 < arr.length && arr[i+1].dataset.audio !== current.dataset.audio) arr[i+1].click(); });
  au.addEventListener('error', function(){ t.textContent = 'לא ניתן לטעון את ההקלטה כרגע'; });
  pp.addEventListener('click', function(){ au.paused ? au.play() : au.pause(); });
  r.addEventListener('input', function(){ if (au.duration) au.currentTime = r.value / 100 * au.duration; });
  sp.addEventListener('click', function(){ si = (si + 1) % speeds.length; au.playbackRate = speeds[si]; sp.textContent = speeds[si] + '×'; });
  bar.querySelector('.lp-x').addEventListener('click', function(){ au.pause(); bar.hidden = true; document.body.classList.remove('lp-on'); mark(null); });

  // ---- read aloud (text to speech) ----
  var synth = window.speechSynthesis, speaking = null;
  function heVoice(){ var v = synth ? synth.getVoices() : []; return v.find(function(x){ return /^he|iw/i.test(x.lang); }); }
  if (synth) synth.onvoiceschanged = function(){};
  function stopTTS(){ if (synth && synth.speaking) synth.cancel(); if (speaking){ speaking.textContent = speaking.dataset.label0; speaking = null; } }
  document.querySelectorAll('[data-tts]').forEach(function(b){
    b.dataset.label0 = b.textContent;
    b.addEventListener('click', function(){
      if (!synth){ b.textContent = 'הדפדפן לא תומך בהקראה'; return; }
      if (speaking === b){ stopTTS(); return; }
      stopTTS(); au.pause();
      var sel = document.querySelectorAll(b.dataset.tts), text = [].map.call(sel, function(p){ return p.textContent; }).join(' ').replace(/[֑-ֽ֯׀׃]/g, '').replace(/׀/g,'');
      var u = new SpeechSynthesisUtterance(text); u.lang = 'he-IL'; var v = heVoice(); if (v) u.voice = v; u.rate = 0.85;
      u.onend = function(){ stopTTS(); };
      speaking = b; b.textContent = '■ עצירת ההקראה';
      synth.speak(u);
      if (!v) setTimeout(function(){ if (speaking === b && !synth.speaking){ b.textContent = 'אין קול עברי במכשיר הזה'; speaking = null; } }, 1500);
    });
  });
})();
