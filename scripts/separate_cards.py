from pathlib import Path
from bs4 import BeautifulSoup
import shutil

path = Path("app/templates/index.html")
html = path.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

def find_heading(name):
    for h in soup.find_all("h2"):
        if h.get_text(" ", strip=True) == name:
            return h
    return None

analytics_h = find_heading("Review Analytics")
history_h = find_heading("Recent reviews")
xai_h = find_heading(
    "Why did the model make this prediction?"
)

if not analytics_h or not history_h:
    raise SystemExit("Required headings missing. No changes made.")

outer = history_h.find_parent("div", class_="card")
analytics_card = analytics_h.find_parent("div", class_="card")

if not outer or not analytics_card:
    raise SystemExit("Expected cards not found.")

if analytics_card.parent != outer:
    raise SystemExit("Unexpected card structure. No changes made.")

# Identify the existing history table container.
history_container = history_h.find_next_sibling("div")

if history_container is None or not history_container.find("table"):
    raise SystemExit(
        "History table container not found. No changes made."
    )

# Move analytics outside the history card.
analytics_card.extract()
outer.insert_before(analytics_card)

# Move Explainable AI outside the history card.
if xai_h:
    xai_card = xai_h.find_parent("div", class_="card")
    if xai_card and xai_card.parent == outer:
        xai_card.extract()
        outer.insert_before(xai_card)

# Existing outer card becomes the history card.
outer["id"] = "reviewHistory"

# Save a backup immediately before writing.
shutil.copy2(
    path,
    "app/templates/index_before_separation.html"
)

path.write_text(str(soup), encoding="utf-8")

print("SUCCESS: Dashboard cards separated!")
