(() => {
  'use strict';

  // Change this value to adjust the pause between consecutive output lines.
  const LINE_DELAY_MS = 50;

  const terminal = document.querySelector('[data-terminal]');
  if (!terminal) return;

  const lines = [...terminal.querySelectorAll('[data-line]')];
  const skip = terminal.querySelector('[data-reveal-skip]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!lines.length || reducedMotion.matches) return;

  let nextLine = 0;
  let timer;
  const showAll = () => {
    window.clearTimeout(timer);
    terminal.classList.remove('is-revealing');
    // Keep keyboard focus in the document when the focused skip button disappears.
    if (document.activeElement === skip) {
      document.querySelector('#main')?.focus({ preventScroll: true });
    }
    if (skip) skip.hidden = true;
  };
  const reveal = () => {
    lines[nextLine].classList.add('is-visible');
    nextLine += 1;
    if (nextLine === lines.length) {
      showAll();
      return;
    }
    timer = window.setTimeout(reveal, LINE_DELAY_MS);
  };

  terminal.classList.add('is-revealing');
  if (skip) {
    skip.hidden = false;
    skip.addEventListener('click', showAll, { once: true });
  }
  reducedMotion.addEventListener('change', event => {
    if (event.matches) showAll();
  });
  window.addEventListener('pagehide', showAll, { once: true });
  reveal();
})();
