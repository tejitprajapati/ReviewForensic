# ReviewGuard AI — B.Tech College Project

A redesigned FastAPI fake-review screening dashboard inspired by the public repository `rithwik-01/fake-review-detector` (see ATTRIBUTION.md). This implementation is new and deliberately simpler to run on Kali Linux.

## Kali Linux: installation

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip unzip
unzip ReviewGuard_AI_College_Project.zip
cd ReviewGuard_AI_College_Project
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Open http://127.0.0.1:8000 in Firefox. API docs: http://127.0.0.1:8000/docs

If the ZIP was extracted into a different folder, `cd` to the directory containing `requirements.txt` before running commands.

## Features
- Review screening with explained flags and simple lexicon sentiment
- FastAPI JSON endpoint `POST /api/analyze` accepting `{"text":"..."}`
- Responsive dashboard and recent analysis history (SQLite)
- Bulk CSV upload/download (CSV header `text`, 500 rows / 2 MB maximum)
- Optional supervised TF-IDF + logistic regression model trained on your own labeled CSV
- Basic unit tests: `python -m unittest discover -s tests`

## Optional ML training
Prepare a **real, appropriately licensed labeled dataset** CSV with columns `text,label`, where 0 means genuine and 1 means fake. Do not use the tiny example CSV as a real dataset. Run:

```bash
python scripts/train_model.py --csv datasets/your_labeled_reviews.csv
```
Restart Uvicorn after training. The dashboard will then use the saved model. Training metrics are printed on a held-out test split; report them only for the actual dataset used. **Never load a joblib file from an untrusted source**.

## Important limitations
- In default mode, the flag score is a rule-derived screening score, **not a probability calibrated on a representative dataset**.
- Even trained classifiers can mistake genuine reviews for fake ones, and can learn dataset artifacts.
- Sentiment does not establish authenticity. Negative reviews can be genuine; positive reviews can be fake.
- **AI-generated text detection is not implemented.** The original repository's `detect_ai.py` is empty, so we do not falsely claim to have LLaMA detection.
- The original repository's README claims metrics but does not provide trained weights in the ZIP. This project makes no accuracy claim until independently evaluated.
- SQLite history contains review text locally. Do not upload private personal information; delete `database/history.db` to clear local history.

## Suggested college report sections
Abstract, problem statement, objectives, literature review, dataset provenance, system architecture, module descriptions, algorithm, experimental methodology, results and confusion matrix, limitations, future scope, references and attribution.

## Future scope
Verified dataset integration, transformer fine-tuning, model calibration, role-based login, human review queue, multilingual review analysis, explainability, and separate AI-authorship research module.
