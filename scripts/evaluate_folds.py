from pathlib import Path
import re
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

source = Path.home() / "Downloads" / "op_spam_v1.4"

texts = []
labels = []
folds = []

for file in sorted(source.rglob("*.txt")):
    path = str(file)

    if "truthful_from_" in path:
        label = 0
    elif "deceptive_from_" in path:
        label = 1
    else:
        continue

    match = re.search(r"fold([1-5])", path)

    if not match:
        continue

    text = file.read_text(
        encoding="utf-8",
        errors="replace"
    ).strip()

    if text:
        texts.append(text)
        labels.append(label)
        folds.append(int(match.group(1)))

texts = np.array(texts)
labels = np.array(labels)
folds = np.array(folds)

print("Total reviews:", len(texts))

if len(texts) != 1600:
    raise ValueError("Expected 1600 reviews. Check dataset.")

scores = []

for fold in range(1, 6):
    train = folds != fold
    test = folds == fold

    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=20000,
            min_df=1
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        ))
    ])

    model.fit(texts[train], labels[train])
    predictions = model.predict(texts[test])

    accuracy = accuracy_score(labels[test], predictions)
    precision = precision_score(
        labels[test], predictions, zero_division=0
    )
    recall = recall_score(
        labels[test], predictions, zero_division=0
    )
    f1 = f1_score(
        labels[test], predictions, zero_division=0
    )

    scores.append([accuracy, precision, recall, f1])

    print(f"\nFold {fold}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    print(f"F1-score: {f1:.2%}")
    print("Confusion matrix:")
    print(confusion_matrix(labels[test], predictions))

scores = np.array(scores)

print("\nAVERAGE RESULTS")
print(f"Accuracy: {scores[:, 0].mean():.2%}")
print(f"Precision: {scores[:, 1].mean():.2%}")
print(f"Recall: {scores[:, 2].mean():.2%}")
print(f"F1-score: {scores[:, 3].mean():.2%}")
