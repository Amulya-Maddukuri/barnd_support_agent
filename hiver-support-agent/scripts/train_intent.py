import argparse, os, sys
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..','src'))
from intents.classifier import IntentClassifier

ap=argparse.ArgumentParser(); ap.add_argument('--data',default='data/golden/amazonhelp_golden_168.csv'); ap.add_argument('--out',default='outputs/intent_model.joblib'); args=ap.parse_args()
df=pd.read_csv(args.data).dropna(subset=['final_intent'])
model=IntentClassifier().fit(df.customer_text.astype(str), df.final_intent.astype(str))
os.makedirs(os.path.dirname(args.out),exist_ok=True); model.save(args.out)
print('trained rows:',len(df),'labels:',df.final_intent.nunique(),'saved:',args.out)
