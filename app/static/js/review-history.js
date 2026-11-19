document.addEventListener("DOMContentLoaded", () => {
  const search = document.getElementById("historySearch");
  const filter = document.getElementById("historyFilter");
  const section = document.getElementById("reviewHistory");
  const counter = document.getElementById("historyCount");

  if (!search || !filter || !section) return;

  const rows = Array.from(
    section.querySelectorAll("tbody tr")
  ).filter(row => row.querySelectorAll("td").length >= 3);

  rows.forEach(row => {
    const cells = row.querySelectorAll("td");
    const label = cells[1].textContent.trim();

    const badge = document.createElement("span");
    badge.className = "cp-history-badge";

    if (label === "Potentially Fake") {
      badge.classList.add("cp-history-fake");
    } else {
      badge.classList.add("cp-history-genuine");
    }

    badge.textContent = label;
    cells[1].replaceChildren(badge);
  });

  function updateHistory() {
    const query = search.value.trim().toLowerCase();
    const selected = filter.value;
    let visible = 0;

    rows.forEach(row => {
      const cells = row.querySelectorAll("td");
      const text = cells[0].textContent.toLowerCase();
      const label = cells[1].textContent.trim();

      const matchesSearch = text.includes(query);

      const matchesFilter =
        selected === "all" ||
        (selected === "fake" && label === "Potentially Fake") ||
        (selected === "genuine" && label === "Likely Genuine");

      const show = matchesSearch && matchesFilter;
      row.hidden = !show;

      if (show) visible++;
    });

    if (counter) {
      counter.textContent =
        `Showing ${visible} of ${rows.length} recent reviews`;
    }
  }

  search.addEventListener("input", updateHistory);
  filter.addEventListener("change", updateHistory);

  updateHistory();
});
