from .explain import explain_prediction
import re
from pathlib import Path
import joblib

POS = {'good','great','excellent','amazing','love','perfect','wonderful','fast','quality','recommend','helpful','best','happy','fantastic'}
NEG = {'bad','poor','terrible','awful','worst','broken','slow','waste','disappointed','fake','refund','horrible','damaged'}
HYPE = {'guaranteed','miracle','unbelievable','life-changing','must-buy','100%','everyone','flawless','perfect'}
MODEL_PATH = Path(__file__).resolve().parent.parent / 'models' / 'review_model.joblib'

def analyze(text):
    text = text.strip()
    if not text: raise ValueError('Review cannot be empty')
    if len(text)>10000: raise ValueError('Review must be under 10,000 characters')
    words = re.findall(r"[a-zA-Z']+", text.lower())
    positive=sum(w in POS for w in words)
    negative=sum(w in NEG for w in words)
    sentiment = 'Positive' if positive>negative else ('Negative' if negative>positive else 'Neutral')
    reasons=[]
    if len(words)<8: reasons.append('Very short review; limited detail')
    if text.count('!')>=3: reasons.append('Excessive exclamation marks')
    if len(words)>5 and len(set(words))/len(words)<0.55: reasons.append('Unusually repetitive wording')
    if sum(w in HYPE for w in words)>=2: reasons.append('Several exaggerated promotional terms')
    if re.search(r'\b(buy now|click here|five stars|5 stars)\b',text,re.I): reasons.append('Contains promotional or rating-pushing language')
    heuristic=min(0.90,0.12+0.16*len(reasons))
    engine='Rule-based screening (not a trained ML prediction)'
    probability=heuristic
    if MODEL_PATH.exists():
        try:
            model=joblib.load(MODEL_PATH)
            probability=float(model.predict_proba([text])[0][list(model.classes_).index(1)])
            engine='Trained TF-IDF + Logistic Regression model'
        except Exception:
            reasons.append('Saved ML model could not be loaded; rules used')
    label='Potentially Fake' if probability>=0.5 else 'Likely Genuine'
    explanations = []
    if engine == 'Trained TF-IDF + Logistic Regression model':
        try:
            explanations = explain_prediction(text)
        except Exception:
            explanations = []

    return {'explanations':explanations,'review':text,'label':label,'score':round(probability*100,1),'sentiment':sentiment,'engine':engine,'reasons':reasons or ['No obvious warning signs detected'], 'ai_detection':'Not available: authorship cannot be reliably inferred from text alone'}
