(() => {
  const root = document.querySelector("[data-slideshow]");
  if (!root) return;

  const slides = [...root.querySelectorAll("[data-slide]")];
  const dots = [...root.querySelectorAll("[data-slideshow-dot]")];
  const prev = root.querySelector("[data-slideshow-prev]");
  const next = root.querySelector("[data-slideshow-next]");
  if (slides.length < 2) return;

  const intervalMs = Number(root.dataset.interval) || 4500;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let index = slides.findIndex((s) => s.classList.contains("is-active"));
  if (index < 0) index = 0;
  let timer = null;

  function show(nextIndex) {
    index = (nextIndex + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      const active = i === index;
      slide.classList.toggle("is-active", active);
      slide.setAttribute("aria-hidden", active ? "false" : "true");
    });
    dots.forEach((dot, i) => {
      const active = i === index;
      dot.classList.toggle("is-active", active);
      if (active) dot.setAttribute("aria-current", "true");
      else dot.removeAttribute("aria-current");
    });
  }

  function stop() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }

  function start() {
    if (reduceMotion) return;
    stop();
    timer = setInterval(() => show(index + 1), intervalMs);
  }

  prev?.addEventListener("click", () => {
    show(index - 1);
    start();
  });
  next?.addEventListener("click", () => {
    show(index + 1);
    start();
  });
  dots.forEach((dot, i) => {
    dot.addEventListener("click", () => {
      show(i);
      start();
    });
  });

  root.addEventListener("mouseenter", stop);
  root.addEventListener("mouseleave", start);
  root.addEventListener("focusin", stop);
  root.addEventListener("focusout", (e) => {
    if (!root.contains(e.relatedTarget)) start();
  });

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stop();
    else start();
  });

  show(index);
  start();
})();
