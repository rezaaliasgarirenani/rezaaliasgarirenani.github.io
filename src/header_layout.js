(() => {
  'use strict';

  const header = document.querySelector('.site-header');
  if (!header) return;
  // Keep fragment links and focused scroll targets below the sticky header,
  // including after resizing, zooming, and navigation wrapping on tablets.
  const update = () => {
    document.documentElement.style.setProperty('--header-height', `${Math.ceil(header.getBoundingClientRect().height)}px`);
  };
  update();
  if ('ResizeObserver' in window) new ResizeObserver(update).observe(header);
  else window.addEventListener('resize', update, { passive: true });
})();
