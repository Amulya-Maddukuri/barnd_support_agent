from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Retriever:
    def __init__(self, texts):
        self.texts=list(texts)
        self.vectorizer=TfidfVectorizer(lowercase=True, ngram_range=(1,2), min_df=1, sublinear_tf=True, max_features=100000)
        self.matrix=self.vectorizer.fit_transform(self.texts)
    def retrieve(self, query, k=5):
        q=self.vectorizer.transform([query])
        sims=cosine_similarity(q,self.matrix).ravel()
        idx=np.argsort(-sims)[:k]
        return [{'text':self.texts[i], 'score':float(sims[i])} for i in idx]
