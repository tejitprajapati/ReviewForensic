document.addEventListener("DOMContentLoaded", () => {
  const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  // Animate review statistics
  const statLabels = [
    "Reviews analyzed",
    "Flagged reviews",
    "Not flagged"
  ];

  document.querySelectorAll(".stat").forEach(card => {
    const label = card.textContent.trim();

    if (!statLabels.some(text => label.includes(text))) return;

    const number = card.querySelector("b, strong");
    if (!number) return;

    const target = Number(number.textContent.trim());
    if (!Number.isFinite(target)) return;

    if (reduceMotion) return;

    const duration = 1100;
    const start = performance.now();

    function animate(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);

      number.textContent = Math.round(target * eased);

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        number.textContent = target;
      }
    }

    requestAnimationFrame(animate);
  });

  // Highlight active navigation link
  const links = document.querySelectorAll(
    "#cyberSidebar .cyber-menu a"
  );

  links.forEach(link => {
    link.addEventListener("click", () => {
      links.forEach(item => item.classList.remove("active"));
      link.classList.add("active");
    });
  });
});

// Phase 6: Prediction animations
document.addEventListener("DOMContentLoaded", () => {
  const result = document.querySelector(".result");

  if (!result) return;

  const pill = result.querySelector(".pill");
  if (!pill) return;

  const prediction = pill.textContent.trim().toLowerCase();

  result.classList.add("cyber-prediction");

  if (prediction.includes("fake")) {
    result.classList.add("fake");
  } else if (prediction.includes("genuine")) {
    result.classList.add("genuine");
  }

  const text = result.textContent;
  const match = text.match(/Flag score:\s*([\d.]+)\s*%/i);

  if (match) {
    const score = Math.max(
      0,
      Math.min(100, parseFloat(match[1]))
    );

    const track = document.createElement("div");
    track.className = "cyber-score-track";

    const fill = document.createElement("div");
    fill.className = "cyber-score-fill";
    fill.setAttribute("role", "progressbar");
    fill.setAttribute("aria-valuemin", "0");
    fill.setAttribute("aria-valuemax", "100");
    fill.setAttribute("aria-valuenow", String(score));
    fill.setAttribute("aria-label", "Review flag score");

    track.appendChild(fill);

    const scoreText = Array.from(
      result.querySelectorAll("p")
    ).find(p => p.textContent.includes("Flag score:"));

    if (scoreText) {
      scoreText.insertAdjacentElement("afterend", track);

      const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
      ).matches;

      if (reduceMotion) {
        fill.style.width = score + "%";
      } else {
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            fill.style.width = score + "%";
          });
        });
      }
    }
  }
});
