(() => {
  'use strict';
  const orbit = document.querySelector('[data-orbit]');
  if (!orbit) return;
  const fallback = orbit.querySelector('[data-orbit-fallback]');
  const image = fallback.querySelector('img');
  const canvas = orbit.querySelector('[data-orbit-canvas]');
  const button = orbit.querySelector('[data-orbit-toggle]');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let player, loading, paused = false, pageActive = true;

  const update = () => {
    const enhanced = Boolean(player) && !reduced.matches;
    fallback.hidden = enhanced;
    canvas.hidden = !enhanced;
    button.hidden = !enhanced;
    button.setAttribute('aria-pressed', String(paused));
    const label = `${paused ? 'Resume' : 'Pause'} Earth animation`;
    button.setAttribute('aria-label', label);
    button.title = label;
    button.querySelector('span').textContent = paused ? '▷' : 'Ⅱ';
    if (!player) return;
    if (enhanced && !paused && !document.hidden && pageActive) {
      if (player.paused) player.play();
    } else player.pause();
  };

  const initialize = async () => {
    if (loading || reduced.matches) return;
    // Keep the original picture available if the player cannot be initialized.
    loading = true;
    try {
      const context = canvas.getContext('2d');
      const parse = window['apng-js']?.default;
      if (!context || !parse) return;
      const response = await fetch(image.src);
      if (!response.ok) throw new Error('Animation unavailable');
      const animation = parse(await response.arrayBuffer());
      if (animation instanceof Error) throw animation;
      player = await animation.getPlayer(context);
      // Release the native animated image after the canvas is ready. The
      // picture remains the static reduced-motion and no-player fallback.
      image.src = fallback.querySelector('source').srcset;
      update();
    } catch {
      // The native image remains visible; never expose an unusable control.
    }
  };

  button.addEventListener('click', () => { paused = !paused; update(); });
  reduced.addEventListener('change', () => { update(); initialize(); });
  document.addEventListener('visibilitychange', update);
  window.addEventListener('pagehide', () => { pageActive = false; update(); });
  window.addEventListener('pageshow', () => { pageActive = true; update(); });
  initialize();
})();
