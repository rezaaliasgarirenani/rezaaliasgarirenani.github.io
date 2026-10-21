(() => {
  'use strict';
  // Local binary rain: no animation library, external requests, or tracking.
  const canvas = document.querySelector('#binary-field');
  const ctx = canvas.getContext('2d');
  const half = document.createElement('canvas');
  const halfCtx = half.getContext('2d');
  const motion = document.querySelector('.motion-toggle');
  if (!ctx || !halfCtx) return;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion:reduce)');
  let enabled = !reducedMotion.matches;
  let inView = true, animation = 0, previousFrame = 0, width = 0, height = 0, columns = [];
  const setMotionLabel = () => {
    motion.setAttribute('aria-label', enabled ? 'Pause animation' : 'Play animation');
    motion.querySelector('.motion-symbol').textContent = enabled ? 'Ⅱ' : '▷';
    motion.querySelector('.motion-label').textContent = enabled ? 'Pause binary motion' : 'Play binary motion';
  };
  const draw = advance => {
    halfCtx.clearRect(0, 0, width, height);
    halfCtx.font = '11px Consolas, monospace';
    columns.forEach((column, index) => {
      if (advance) {
        column.y += column.speed;
        if (column.y > height + column.length * 22) column.y = -22;
        if (Math.random() < .13) column.bits[Math.floor(Math.random() * column.bits.length)] = Math.random() > .5 ? '1' : '0';
      }
      for (let row = 0; row < column.length; row++) {
        const y = column.y - row * 22;
        if (y < 0 || y > height) continue;
        halfCtx.fillStyle = `rgba(88,166,255,${(1 - row / column.length) * (index % 4 === 0 ? .55 : .27)})`;
        halfCtx.fillText(column.bits[row], index * 22 + 7, y);
      }
    });
    // Reflect the same pixels so brightness, digits, and motion match exactly.
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(half, 0, 0);
    ctx.save();
    ctx.translate(canvas.width, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(half, 0, 0);
    ctx.restore();
  };
  const resize = () => {
    const bounds = canvas.getBoundingClientRect();
    width = bounds.width; height = bounds.height;
    const scale = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * scale); canvas.height = Math.round(height * scale);
    half.width = Math.ceil(canvas.width / 2); half.height = canvas.height;
    halfCtx.setTransform(scale, 0, 0, scale, 0, 0);
    columns = Array.from({ length: Math.ceil(half.width / scale / 22) }, () => {
      const length = 9 + Math.floor(Math.random() * 18);
      return { y: Math.random() * (height + 300), speed: 1 + Math.random() * 2.5, length, bits: Array.from({ length }, () => Math.random() > .5 ? '1' : '0') };
    });
    draw(false);
  };
  const frame = time => {
    animation = 0;
    if (!enabled || document.hidden || !inView) return;
    if (time - previousFrame > 65) { draw(true); previousFrame = time; }
    animation = window.requestAnimationFrame(frame);
  };
  const sync = () => {
    window.cancelAnimationFrame(animation); animation = 0;
    if (enabled && !document.hidden && inView) animation = window.requestAnimationFrame(frame);
  };
  motion.hidden = false;
  motion.addEventListener('click', () => { enabled = !enabled; setMotionLabel(); sync(); });
  reducedMotion.addEventListener('change', () => { enabled = !reducedMotion.matches; setMotionLabel(); sync(); });
  document.addEventListener('visibilitychange', sync);
  new IntersectionObserver(entries => { inView = entries[0].isIntersecting; sync(); }).observe(canvas);
  new ResizeObserver(resize).observe(canvas);
  resize(); setMotionLabel(); sync();
})();
