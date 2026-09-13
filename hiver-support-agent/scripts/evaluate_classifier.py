"""Evaluate intent baselines on the curated AmazonHelp set.
Uses 5-fold stratified CV to avoid depending on a single small holdout.
"""
import argparse, os, json
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--data',default='data/golden/amazonhelp_golden_168.csv')
    ap.add_argument('--out',default='outputs/intent_metrics.json')
    args=ap.parse_args()
    df=pd.read_csv(args.data).fillna('')
    X=df.customer_text.astype(str).values
    y=df.final_intent.astype(str).values
    skf=StratifiedKFold(n_splits=5,shuffle=True,random_state=42)
    results={"folds":5,"n_examples":len(df),"classes":sorted(set(y)),"models":{}}
    for name, builder in [
        ('majority', lambda: DummyClassifier(strategy='most_frequent')),
        ('tfidf_logreg', lambda: Pipeline([
            ('tfidf',TfidfVectorizer(lowercase=True,ngram_range=(1,2),sublinear_tf=True,min_df=1,max_features=50000)),
            ('clf',LogisticRegression(max_iter=1500,class_weight='balanced'))
        ]))]:
        acc=[]; f1=[]
        for tr,te in skf.split(X,y):
            m=builder().fit(X[tr],y[tr]); p=m.predict(X[te])
            acc.append(accuracy_score(y[te],p)); f1.append(f1_score(y[te],p,average='macro',zero_division=0))
        results['models'][name]={
            'accuracy_mean':float(sum(acc)/len(acc)),
            'accuracy_std':float(pd.Series(acc).std(ddof=1)),
            'macro_f1_mean':float(sum(f1)/len(f1)),
            'macro_f1_std':float(pd.Series(f1).std(ddof=1)),
            'fold_accuracy':acc,
            'fold_macro_f1':f1,
        }
    os.makedirs(os.path.dirname(args.out),exist_ok=True)
    with open(args.out,'w') as f: json.dump(results,f,indent=2)
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
