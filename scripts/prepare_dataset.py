import csv
from pathlib import Path

source = Path.home() / "Downloads" / "op_spam_v1.4"
output = Path("datasets/hotel_reviews.csv")

rows = []

for file in sorted(source.rglob("*.txt")):
    path = str(file)

    if "truthful_from_" in path:
        label = 0
    elif "deceptive_from_" in path:
        label = 1
    else:
        continue

    text = file.read_text(
        encoding="utf-8", errors="replace"
    ).strip()

    if text:
        rows.append([text, label])

output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "label"])
    writer.writerows(rows)

print("Dataset created successfully!")
print("Total reviews:", len(rows))
print("Genuine reviews:", sum(r[1] == 0 for r in rows))
print("Fake reviews:", sum(r[1] == 1 for r in rows))
print("Saved to:", output)
