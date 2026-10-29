(() => {
  'use strict';

  const clocks = [...document.querySelectorAll('[data-clock]')].map(element => ({
    element,
    formatter: new Intl.DateTimeFormat('en-GB', {
      timeZone: element.dataset.timeZone,
      hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23',
    }),
  }));
  if (!clocks.length) return;

  let timer;
  let pageActive = true;
  const update = () => {
    window.clearTimeout(timer);
    const now = new Date();
    clocks.forEach(({ element, formatter }) => {
      element.textContent = formatter.format(now);
      element.dateTime = now.toISOString();
    });
    if (!document.hidden && pageActive) {
      timer = window.setTimeout(update, 1000 - Date.now() % 1000);
    }
  };

  document.addEventListener('visibilitychange', update);
  window.addEventListener('pagehide', () => { pageActive = false; window.clearTimeout(timer); });
  window.addEventListener('pageshow', () => { pageActive = true; update(); });
  update();
})();
