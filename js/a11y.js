/* Accessibility menu (IS 5568 / WCAG 2.0 AA helpers) – no third-party overlay. Settings persist per visitor. */
(function(){
  var KEY = 'a11yPrefs', root = document.documentElement, prefs = {};
  try { prefs = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch(e){ prefs = {}; }
  function save(){ try { localStorage.setItem(KEY, JSON.stringify(prefs)); } catch(e){} }
  function apply(){
    root.style.setProperty('--a11y-scale', String(1 + (prefs.text || 0) * 0.12));
    root.classList.toggle('a11y-text', !!prefs.text);
    root.classList.toggle('a11y-contrast', !!prefs.contrast);
    root.classList.toggle('a11y-links', !!prefs.links);
    root.classList.toggle('a11y-font', !!prefs.font);
    root.classList.toggle('a11y-still', !!prefs.still);
    document.querySelectorAll('video[autoplay], #heroVid').forEach(function(v){ if (prefs.still) v.pause(); });
    if (panel) panel.querySelectorAll('[data-a]').forEach(function(b){
      var k = b.dataset.a; var on = k === 'text' ? (prefs.text || 0) > 0 : !!prefs[k];
      b.setAttribute('aria-pressed', on);
      if (k === 'text') b.querySelector('small').textContent = prefs.text ? ('רמה ' + prefs.text) : '';
    });
  }

  // skip link
  var main = document.querySelector('main');
  if (main){
    if (!main.id) main.id = 'top';
    main.setAttribute('tabindex', '-1');
    var skip = document.createElement('a');
    skip.className = 'skip'; skip.href = '#' + main.id; skip.textContent = 'דלג לתוכן הראשי';
    document.body.insertBefore(skip, document.body.firstChild);
  }

  // menu
  var btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'a11y-btn'; btn.setAttribute('aria-label', 'תפריט נגישות'); btn.setAttribute('aria-expanded', 'false'); btn.setAttribute('aria-controls', 'a11yPanel');
  btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="4" r="2" fill="currentColor"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M5 8l7 1.5L19 8M12 9.5V14m0 0l-3 7m3-7l3 7"/></svg>';
  var panel = document.createElement('div');
  panel.className = 'a11y-panel'; panel.id = 'a11yPanel'; panel.hidden = true; panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', 'הגדרות נגישות');
  panel.innerHTML =
    '<div class="a11y-h"><b>נגישות</b><button type="button" class="a11y-x" aria-label="סגירת תפריט הנגישות">✕</button></div>' +
    '<button type="button" data-a="text" aria-pressed="false">הגדלת טקסט <small></small></button>' +
    '<button type="button" data-a="contrast" aria-pressed="false">ניגודיות גבוהה</button>' +
    '<button type="button" data-a="links" aria-pressed="false">הדגשת קישורים</button>' +
    '<button type="button" data-a="font" aria-pressed="false">גופן קריא</button>' +
    '<button type="button" data-a="still" aria-pressed="false">עצירת אנימציות ווידאו</button>' +
    '<button type="button" data-a="reset">איפוס הגדרות</button>' +
    '<a href="/negishut/">הצהרת נגישות</a>';
  document.body.appendChild(btn); document.body.appendChild(panel);

  function setOpen(o){ panel.hidden = !o; btn.setAttribute('aria-expanded', o); if (o) panel.querySelector('[data-a]').focus(); }
  btn.addEventListener('click', function(){ setOpen(panel.hidden); });
  panel.querySelector('.a11y-x').addEventListener('click', function(){ setOpen(false); btn.focus(); });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && !panel.hidden){ setOpen(false); btn.focus(); } });
  panel.addEventListener('click', function(e){
    var b = e.target.closest('[data-a]'); if (!b) return;
    var k = b.dataset.a;
    if (k === 'reset') prefs = {};
    else if (k === 'text') prefs.text = ((prefs.text || 0) + 1) % 4;
    else prefs[k] = !prefs[k];
    save(); apply();
  });
  apply();
})();
