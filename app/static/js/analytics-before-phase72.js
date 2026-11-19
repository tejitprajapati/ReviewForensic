document.addEventListener("DOMContentLoaded", () => {
  const chart = document.getElementById("reviewChart");

  if (!chart) return;

  chart.style.cursor = "pointer";
  chart.setAttribute("title", "Click to view review statistics");
  chart.setAttribute("tabindex", "0");
  chart.setAttribute("role", "button");

  function showStatistics() {
    const fake = Number(chart.dataset.fake || 0);
    const genuine = Number(chart.dataset.genuine || 0);
    const total = fake + genuine;

    const fakePercent = total
      ? ((fake / total) * 100).toFixed(1)
      : "0.0";

    alert(
      "ReviewGuard AI — Analytics\n\n" +
      "Total reviews: " + total + "\n" +
      "Flagged reviews: " + fake + "\n" +
      "Not flagged: " + genuine + "\n" +
      "Flagged percentage: " + fakePercent + "%"
    );
  }

  chart.addEventListener("click", showStatistics);

  chart.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      showStatistics();
    }
  });
});
