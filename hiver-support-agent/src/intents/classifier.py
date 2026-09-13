from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

class IntentClassifier:
    def __init__(self):
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(lowercase=True, ngram_range=(1,2), min_df=2, sublinear_tf=True, max_features=50000)),
            ('clf', LogisticRegression(max_iter=1000, class_weight='balanced'))
        ])
    def fit(self, texts, labels):
        self.model.fit(texts, labels); return self
    def predict(self, texts): return self.model.predict(texts)
    def predict_proba(self, texts): return self.model.predict_proba(texts)
    def save(self, path): joblib.dump(self.model, path)
    @classmethod
    def load(cls, path):
        x=cls(); x.model=joblib.load(path); return x
