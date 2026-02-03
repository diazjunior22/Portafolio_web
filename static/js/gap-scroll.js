// Gap Scroll: adds vertical spacing between sections when scrolling to anchors
(function(){
  // Configurable gap in px (align with CSS var --gap-size)
  const gap = 96; // px
  // Smoothly scrolls with offset
  function smoothScrollTo(hash) {
    const el = document.querySelector(hash);
    if (el) {
      const y = el.getBoundingClientRect().top + window.pageYOffset - gap;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  }
  // Attach to in-page anchors
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function(e){
      const hash = this.getAttribute('href');
      if (hash.length > 1 && document.querySelector(hash)) {
        e.preventDefault();
        smoothScrollTo(hash);
      }
    });
  });
  // Initial highlight of anchored sections (optional)
})();
