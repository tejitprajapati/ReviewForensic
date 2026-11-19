# Project overview

**Title:** ReviewGuard AI: Review Authenticity Screening and Sentiment Dashboard

**Problem:** Online reviews can be misleading. Screening models may assist manual moderation, but no classifier can prove a review is fraudulent solely from text.

**Architecture:** Browser -> FastAPI -> analyzer.py (rules or optional TF-IDF classifier) -> SQLite history. CSV upload -> analysis -> CSV results download.

**Modules:** 1. Dashboard 2. Single review analyzer 3. CSV batch analysis 4. Sentiment lexicon 5. Local history 6. Optional supervised ML training 7. JSON API.

**Viva talking points:** Difference between heuristics and trained ML; TF-IDF feature representation; logistic regression; precision vs recall; why train/test split matters; limitations and class imbalance; false positives; why sentiment is not authenticity; ethical handling of reviews.

**Demo sequence:** Start server; enter a short review; explain reasons and score; enter a longer review; upload a CSV with `text` header; show saved history; open `/docs`; optionally train on a sufficiently large real labeled dataset and compare results.
