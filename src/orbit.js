(() => {
  'use strict';
  const orbit = document.querySelector('[data-orbit]');
  const motion = window.siteMotion;
  if (!orbit || !motion) return;
  const fallback = orbit.querySelector('[data-orbit-fallback]');
  const image = fallback.querySelector('img');
  const animationURL = image.getAttribute('src');
  const stillURL = fallback.querySelector('source').srcset;
  const canvas = orbit.querySelector('[data-orbit-canvas]');
  const button = orbit.querySelector('[data-orbit-toggle]');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let player, loading, pageActive = true;

  const update = () => {
    const enhanced = Boolean(player) && !reduced.matches;
    fallback.hidden = enhanced;
    canvas.hidden = !enhanced;
    button.hidden = !enhanced;
    // Also stop the native fallback if paused before the canvas is ready.
    const source = player || motion.paused ? stillURL : animationURL;
    if (image.getAttribute('src') !== source) image.src = source;
    if (!player) return;
    if (enhanced && !motion.paused && !document.hidden && pageActive) {
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
      const response = await fetch(animationURL);
      if (!response.ok) throw new Error('Animation unavailable');
      const animation = parse(await response.arrayBuffer());
      if (animation instanceof Error) throw animation;
      player = await animation.getPlayer(context);
      // Release the native animated image after the canvas is ready. The
      // picture remains the static reduced-motion and no-player fallback.
      update();
    } catch {
      // The native image remains visible; never expose an unusable control.
    }
  };

  document.addEventListener('site-motion-change', update);
  reduced.addEventListener('change', () => { update(); initialize(); });
  document.addEventListener('visibilitychange', update);
  window.addEventListener('pagehide', () => { pageActive = false; update(); });
  window.addEventListener('pageshow', () => { pageActive = true; update(); });
  update(); initialize();
})();
