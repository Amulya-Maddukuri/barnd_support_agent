import pandas as pd, re, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from src.agent.escalation import decide_escalation

p='data/golden/amazonhelp_golden_168.csv'
df=pd.read_csv(p).fillna('')
rows=[]
for _,r in df.iterrows():
    pred, reason=decide_escalation(r.customer_text,r.final_intent,confidence=0.9,evidence_score=0.5)
    rows.append(pred)
y=[x=='yes' for x in df.escalation_gold]
p=rows
pr,re,f1,_=precision_recall_fscore_support(y,p,average='binary',zero_division=0)
out={'accuracy':accuracy_score(y,p),'precision':pr,'recall':re,'f1':f1,'n':len(df),'positive_gold':sum(y)}
os.makedirs('outputs',exist_ok=True)
json.dump(out,open('outputs/escalation_metrics.json','w'),indent=2)
print(json.dumps(out,indent=2))
