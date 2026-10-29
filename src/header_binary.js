(() => {
  'use strict';

  const strip = document.querySelector('[data-binary-strip]');
  const toggle = document.querySelector('[data-binary-toggle]');
  if (!strip || !toggle) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let userPaused = false;
  let inView = true;

  const update = () => {
    strip.classList.toggle('has-motion', !reducedMotion.matches);
    strip.classList.toggle('is-paused', userPaused || document.hidden || !inView);
    toggle.hidden = reducedMotion.matches;
    const label = userPaused ? 'Resume header animation' : 'Pause header animation';
    toggle.setAttribute('aria-label', label);
    toggle.title = label;
    toggle.querySelector('span').textContent = userPaused ? '▷' : 'Ⅱ';
  };

  toggle.addEventListener('click', () => {
    userPaused = !userPaused;
    update();
  });
  reducedMotion.addEventListener('change', update);
  document.addEventListener('visibilitychange', update);

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      inView = entries[0].isIntersecting;
      update();
    }).observe(strip);
  }

  update();
})();
