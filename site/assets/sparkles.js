const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
let lastSparkle = 0;

addEventListener('pointermove', event => {
  if (reducedMotion.matches || event.pointerType === 'touch' || event.timeStamp - lastSparkle < 40) return;
  lastSparkle = event.timeStamp;
  const star = document.createElement('span');
  star.className = 'cursor-star';
  star.textContent = ['✧', '✦', '⋆'][Math.floor(Math.random() * 3)];
  star.setAttribute('aria-hidden', 'true');
  star.style.left = `${event.clientX}px`;
  star.style.top = `${event.clientY}px`;
  document.body.append(star);
  setTimeout(() => star.remove(), 700);
});
