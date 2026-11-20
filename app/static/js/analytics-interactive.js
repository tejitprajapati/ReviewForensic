document.addEventListener("DOMContentLoaded", () => {
  const chart = document.getElementById("reviewChart");
  if (!chart) return;

  chart.style.cursor = "pointer";
  chart.setAttribute("tabindex", "0");
  chart.setAttribute("role", "button");
  chart.setAttribute("aria-label", "View review statistics");

  const overlay = document.createElement("div");
  overlay.className = "cp-analytics-overlay";
  overlay.hidden = true;

  overlay.innerHTML = `
    <section class="cp-analytics-modal"
             role="dialog"
             aria-modal="true"
             aria-labelledby="cp-modal-title">
      <button class="cp-modal-close"
              type="button"
              aria-label="Close analytics">×</button>
      <div class="cp-modal-eyebrow">◆ REVIEWFORENSIC INTELLIGENCE</div>
      <h2 id="cp-modal-title">Review Analytics</h2>
      <p class="cp-modal-subtitle">
        Live statistics from your review history
      </p>

      <div class="cp-modal-stats">
        <div><strong id="cp-total">0</strong><span>Total</span></div>
        <div><strong id="cp-fake">0</strong><span>Flagged</span></div>
        <div><strong id="cp-genuine">0</strong><span>Not flagged</span></div>
      </div>

      <div class="cp-progress-heading">
        <span>Flagged reviews</span>
        <strong id="cp-percent">0%</strong>
      </div>
      <div class="cp-progress-track">
        <div id="cp-progress-fill"></div>
      </div>
      <p class="cp-modal-note">
        Predictions are screening indicators, not verified findings.
      </p>
    </section>
  `;

  document.body.appendChild(overlay);

  const closeButton = overlay.querySelector(".cp-modal-close");
  let previousFocus = null;

  function closeModal() {
    overlay.hidden = true;
    document.body.classList.remove("cp-modal-open");
    if (previousFocus) previousFocus.focus();
  }

  function openModal() {
    const fake = Number(chart.dataset.fake || 0);
    const genuine = Number(chart.dataset.genuine || 0);
    const total = fake + genuine;
    const percent = total ? (fake / total) * 100 : 0;

    overlay.querySelector("#cp-total").textContent = total;
    overlay.querySelector("#cp-fake").textContent = fake;
    overlay.querySelector("#cp-genuine").textContent = genuine;
    overlay.querySelector("#cp-percent").textContent =
      percent.toFixed(1) + "%";

    previousFocus = document.activeElement;
    overlay.hidden = false;
    document.body.classList.add("cp-modal-open");

    const bar = overlay.querySelector("#cp-progress-fill");
    bar.style.width = "0%";

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        bar.style.width = percent + "%";
      });
    });

    closeButton.focus();
  }

  chart.addEventListener("click", openModal);

  chart.addEventListener("keydown", event => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openModal();
    }
  });

  closeButton.addEventListener("click", closeModal);

  overlay.addEventListener("click", event => {
    if (event.target === overlay) closeModal();
  });

  document.addEventListener("keydown", event => {
    if (overlay.hidden) return;

    if (event.key === "Escape") {
      closeModal();
    } else if (event.key === "Tab") {
      event.preventDefault();
      closeButton.focus();
    }
  });
});
