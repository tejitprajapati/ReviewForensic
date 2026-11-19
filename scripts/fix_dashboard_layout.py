from pathlib import Path
from bs4 import BeautifulSoup
import shutil

path = Path("app/templates/index.html")
backup = Path("app/templates/index_layout_backup.html")

html = path.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

headings = {
    h.get_text(" ", strip=True): h
    for h in soup.find_all("h2")
}

required = [
    "Review Analytics",
    "Why did the model make this prediction?",
    "Recent reviews"
]

missing = [h for h in required if h not in headings]

if missing:
    raise SystemExit(f"Missing headings: {missing}")

analytics = headings["Review Analytics"]
history = headings["Recent reviews"]
xai = headings["Why did the model make this prediction?"]

outer = analytics.find_parent("div", class_="card")
xai_card = xai.find_parent("div", class_="card")

if outer is None or xai_card is None:
    raise SystemExit("Expected cards not found.")

if history.find_parent("div", class_="card") != outer:
    raise SystemExit("Unexpected history structure.")

if xai_card.parent != outer:
    raise SystemExit("Unexpected explanation structure.")

if outer.find_parent("div", class_="card"):
    raise SystemExit("Unexpected nested analytics parent.")

# Locate the actual review history table.
table = history.find_next_sibling("div")

if table is None or table.name != "div":
    table = history.find_next_sibling("table")

if table is None:
    raise SystemExit(
        "History table container not found. No changes made."
    )

# Create independent cards.
history_card = soup.new_tag("div")
history_card["class"] = ["card"]
history_card["id"] = "reviewHistory"

history.extract()
table.extract()

history_card.append(history)
history_card.append(table)

# Move explanation card outside analytics.
xai_card.extract()

outer.insert_after(history_card)
outer.insert_after(xai_card)

# Save only after structural checks.
shutil.copy2(path, backup)
path.write_text(str(soup), encoding="utf-8")

print("Dashboard layout updated successfully!")
print("Backup:", backup)
