"use strict";

(() => {
  const themes = __THEMES__;
  const intervalMs = __INTERVAL_MS__;
  const root = document.documentElement;
  const parameters = new URLSearchParams(location.search);
  const themedBackground = parameters.get("background") === "theme";
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  let current = themes.findIndex((theme) => theme.id === "classic-light");
  let timer;

  function applyTheme() {
    const theme = themes[current];
    root.dataset.theme = theme.id;
    root.style.setProperty("--splash-text", theme.text);
    root.style.setProperty("--splash-accent", theme.accent);
    root.style.setProperty(
      "--splash-background", themedBackground ? theme.background : "transparent"
    );
  }

  function nextTheme() {
    // Sample all other themes with equal probability, avoiding immediate repeats.
    const offset = 1 + Math.floor(Math.random() * (themes.length - 1));
    current = (current + offset) % themes.length;
    applyTheme();
  }

  function updateTimer() {
    clearInterval(timer);
    if (!reducedMotion.matches && !document.hidden) {
      timer = setInterval(nextTheme, intervalMs);
    }
  }

  applyTheme();
  reducedMotion.addEventListener("change", updateTimer);
  document.addEventListener("visibilitychange", updateTimer);
  addEventListener("pagehide", () => clearInterval(timer));
  addEventListener("pageshow", updateTimer);
  updateTimer();
})();
