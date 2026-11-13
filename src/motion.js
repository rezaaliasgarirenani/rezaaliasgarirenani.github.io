(() => {
  'use strict';
  let paused = false;
  window.siteMotion = Object.freeze({ get paused() { return paused; } });
  const buttons = [...document.querySelectorAll('[data-rail-toggle], [data-orbit-toggle]')];
  const targets = [...document.querySelectorAll('.binary-strip[id], [data-orbit-canvas][id]')]
    .map(element => element.id).join(' ');
  const render = () => {
    buttons.forEach(button => {
      const label = `${paused ? 'Resume' : 'Pause'} all animations`;
      button.setAttribute('aria-pressed', String(paused));
      button.setAttribute('aria-controls', targets);
      button.setAttribute('aria-label', label);
      button.title = label;
      button.querySelector('span').textContent = paused ? '▷' : 'Ⅱ';
    });
  };
  buttons.forEach(button => button.addEventListener('click', () => {
    paused = !paused;
    render();
    document.dispatchEvent(new Event('site-motion-change'));
  }));
  render();
})();
