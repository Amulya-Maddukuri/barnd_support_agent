import argparse, os, sys, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..','src'))
from intents.classifier import IntentClassifier
from retrieval.retrieve import Retriever
from agent.generator import draft_reply
from agent.escalation import decide_escalation

ap=argparse.ArgumentParser(); ap.add_argument('--message',required=True); ap.add_argument('--data',default='data/golden/amazonhelp_golden_168.csv'); ap.add_argument('--model',default='outputs/intent_model.joblib'); args=ap.parse_args()
if not os.path.exists(args.model):
    raise SystemExit('Train first: python scripts/train_intent.py')
df=pd.read_csv(args.data).fillna('')
clf=IntentClassifier.load(args.model)
intent=clf.predict([args.message])[0]; conf=float(clf.predict_proba([args.message]).max())
retr=Retriever(df.customer_text.tolist()); evidence=retr.retrieve(args.message,k=3)
reply=draft_reply(args.message,intent,evidence)
esc,reason=decide_escalation(args.message,intent,conf,evidence[0]['score'] if evidence else 0)
print({'intent':intent,'confidence':round(conf,3),'escalate':esc,'reason':reason,'evidence':evidence,'reply':reply})
