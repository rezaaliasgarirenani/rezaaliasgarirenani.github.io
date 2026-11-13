(() => {
  'use strict';
  const motion = window.siteMotion;
  if (!motion) return;
  const SPEED_PX_PER_SECOND = 60;
  const DIGIT_UPDATE_MS = 70;
  const CELL_HEIGHT_PX = 14;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let pageActive = true;
  const rails = [...document.querySelectorAll('[data-binary-rail]')].map(element => {
    const strip = element.querySelector('.binary-strip');
    const sequences = [...strip.querySelectorAll('.binary-sequence')];
    const buttons = [...element.querySelectorAll('[data-rail-toggle]')];
    let timer = 0, height = 0, digits = [];
    const render = () => sequences.forEach(s => { s.textContent = digits.join('\n'); });
    const resize = () => {
      const nextHeight = Math.max(CELL_HEIGHT_PX, Math.ceil(strip.clientHeight / CELL_HEIGHT_PX) * CELL_HEIGHT_PX);
      if (height === nextHeight) return;
      // Keep the paused frame intact; apply a deferred resize when running again.
      if (height && !running()) return;
      height = nextHeight;
      strip.style.setProperty('--binary-height', `${height}px`);
      strip.style.setProperty('--binary-duration', `${height / SPEED_PX_PER_SECOND}s`);
      digits = Array.from({ length: height / CELL_HEIGHT_PX }, () => Math.random() < .5 ? '0' : '1');
      render();
    };
    const running = () => !reduced.matches && !motion.paused && !document.hidden && pageActive;
    const mutate = () => {
      timer = 0;
      if (!running()) return;
      const indices = new Set();
      const count = Math.max(1, Math.ceil(digits.length / 5));
      while (indices.size < count) indices.add(Math.floor(Math.random() * digits.length));
      indices.forEach(i => { digits[i] = digits[i] === '0' ? '1' : '0'; });
      render();
      timer = window.setTimeout(mutate, DIGIT_UPDATE_MS);
    };
    const update = () => {
      if (running()) resize();
      strip.classList.toggle('has-motion', !reduced.matches);
      strip.classList.toggle('is-paused', !running());
      buttons.forEach(button => {
        button.hidden = reduced.matches;
      });
      if (running() && !timer) timer = window.setTimeout(mutate, DIGIT_UPDATE_MS);
      if (!running()) { window.clearTimeout(timer); timer = 0; }
    };
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(strip);
    else window.addEventListener('resize', resize);
    resize(); update();
    return { update };
  });
  const update = () => rails.forEach(rail => rail.update());
  document.addEventListener('site-motion-change', update);
  reduced.addEventListener('change', update);
  document.addEventListener('visibilitychange', update);
  window.addEventListener('pagehide', () => { pageActive = false; update(); });
  window.addEventListener('pageshow', () => { pageActive = true; update(); });
})();
