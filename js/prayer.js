(function(){
  var t = document.getElementById('prText'); if (!t) return;
  var KEY = 'prayerFs', fs = 1;
  try { fs = parseFloat(localStorage.getItem(KEY)) || 1; } catch(e){}
  function apply(){ t.style.setProperty('--fs', fs); try { localStorage.setItem(KEY, fs); } catch(e){} }
  apply();
  t.addEventListener('click', function(e){
    var b = e.target.closest('button'); if (!b) return;
    if (b.dataset.fs){ fs = Math.min(1.8, Math.max(.8, fs + (+b.dataset.fs)*0.1)); apply(); }
    if (b.hasAttribute('data-print')) window.print();
    if (b.hasAttribute('data-share')){
      var u = location.href.split('#')[0], title = document.querySelector('h1').textContent;
      if (navigator.share) navigator.share({title: title, url: u}).catch(function(){});
      else window.open('https://wa.me/?text=' + encodeURIComponent(title + ' – ' + u), '_blank', 'noopener');
    }
  });
})();
