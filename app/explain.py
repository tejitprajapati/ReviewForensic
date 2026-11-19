from pathlib import Path
import joblib

MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "review_model.joblib"
)

def explain_prediction(text, top_n=5):
    if not MODEL_PATH.exists():
        return []

    model = joblib.load(MODEL_PATH)

    vectorizer = model.named_steps["tfidf"]
    classifier = model.named_steps["clf"]

    vector = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()

    if list(classifier.classes_) != [0, 1]:
        return []

    contributions = vector.multiply(
        classifier.coef_[0]
    ).tocoo()

    terms = []

    for index, value in zip(
        contributions.col,
        contributions.data
    ):
        terms.append({
            "word": str(feature_names[index]),
            "impact": round(float(value), 4),
            "direction": (
                "Fake" if value > 0 else "Genuine"
            )
        })

    terms.sort(
        key=lambda item: abs(item["impact"]),
        reverse=True
    )

    return terms[:top_n]
