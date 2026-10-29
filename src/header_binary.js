(() => {
  'use strict';

  const SPEED_PX_PER_SECOND = 60;
  const DIGIT_UPDATE_MS = 70;
  const CELL_WIDTH_PX = 8;

  const strip = document.querySelector('[data-binary-strip]');
  const toggle = document.querySelector('[data-binary-toggle]');
  if (!strip || !toggle) return;
  const sequences = [...strip.querySelectorAll('.binary-sequence')];
  if (sequences.length !== 2) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let userPaused = false;
  let inView = true;
  let pageActive = true;
  let mutationTimer = 0;
  let currentWidth = 0;
  let digits = [];

  const running = () => !reducedMotion.matches && !userPaused && !document.hidden && inView && pageActive;
  const render = () => {
    const text = digits.join('');
    sequences.forEach(sequence => { sequence.textContent = text; });
  };
  const resize = () => {
    const width = Math.max(CELL_WIDTH_PX, Math.ceil(strip.clientWidth / CELL_WIDTH_PX) * CELL_WIDTH_PX);
    if (width === currentWidth) return;
    currentWidth = width;
    strip.style.setProperty('--binary-width', `${width}px`);
    strip.style.setProperty('--binary-duration', `${width / SPEED_PX_PER_SECOND}s`);
    digits = Array.from({ length: width / CELL_WIDTH_PX }, () => Math.random() < .5 ? '0' : '1');
    render();
  };
  const mutate = () => {
    mutationTimer = 0;
    if (!running()) return;
    const changes = new Set();
    const count = Math.max(1, Math.ceil(digits.length / 5));
    while (changes.size < count) changes.add(Math.floor(Math.random() * digits.length));
    changes.forEach(index => { digits[index] = digits[index] === '0' ? '1' : '0'; });
    render();
    mutationTimer = window.setTimeout(mutate, DIGIT_UPDATE_MS);
  };
  const update = () => {
    const active = running();
    strip.classList.toggle('has-motion', !reducedMotion.matches);
    strip.classList.toggle('is-paused', !active);
    toggle.hidden = reducedMotion.matches;
    const label = userPaused ? 'Resume header animation' : 'Pause header animation';
    toggle.setAttribute('aria-label', label);
    toggle.title = label;
    toggle.querySelector('span').textContent = userPaused ? '▷' : 'Ⅱ';
    if (active && !mutationTimer) mutationTimer = window.setTimeout(mutate, DIGIT_UPDATE_MS);
    if (!active) {
      window.clearTimeout(mutationTimer);
      mutationTimer = 0;
    }
  };

  toggle.addEventListener('click', () => { userPaused = !userPaused; update(); });
  reducedMotion.addEventListener('change', update);
  document.addEventListener('visibilitychange', update);
  window.addEventListener('pagehide', () => { pageActive = false; update(); });
  window.addEventListener('pageshow', () => { pageActive = true; update(); });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => { inView = entries[0].isIntersecting; update(); }).observe(strip);
  }
  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(strip);
  else window.addEventListener('resize', resize);

  resize();
  update();
})();
