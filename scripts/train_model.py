import argparse, csv
from pathlib import Path
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

parser=argparse.ArgumentParser(description='Train model using labeled CSV columns text,label (0=genuine, 1=fake)')
parser.add_argument('--csv',required=True)
args=parser.parse_args()
texts=[];labels=[]
with open(args.csv,encoding='utf-8-sig',newline='') as f:
    for row in csv.DictReader(f):
        try:
            label=int(row['label']);text=row['text'].strip()
            if label in (0,1) and text: texts.append(text);labels.append(label)
        except (KeyError,ValueError,AttributeError):pass
if len(texts)<20 or min(labels.count(0),labels.count(1))<5:
    raise SystemExit('Need at least 20 labeled reviews and at least 5 of each class.')
X_train,X_test,y_train,y_test=train_test_split(texts,labels,test_size=.25,random_state=42,stratify=labels)
model=Pipeline([('tfidf',TfidfVectorizer(ngram_range=(1,2),max_features=20000,min_df=1)),('clf',LogisticRegression(max_iter=1000,class_weight='balanced'))])
model.fit(X_train,y_train)
print(classification_report(y_test,model.predict(X_test),zero_division=0))
print('Confusion matrix:',confusion_matrix(y_test,model.predict(X_test)).tolist())
path=Path(__file__).resolve().parent.parent/'models'/'review_model.joblib';path.parent.mkdir(exist_ok=True);joblib.dump(model,path)
print('Model saved:',path)
print('Note: Evaluate on independent, representative data before making performance claims.')
