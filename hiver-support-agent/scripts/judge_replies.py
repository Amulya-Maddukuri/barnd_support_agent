"""LLM-as-judge harness.
Input CSV columns: customer_text, draft_reply, evidence_text.
The judge scores relevance, groundedness, helpfulness, accuracy and tone (1-5).
Optionally compare judge scores with human_* columns using Spearman correlation.
"""
import argparse, json, os
import pandas as pd

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--output',default='outputs/reply_judge.json'); args=ap.parse_args()
    from openai import OpenAI
    if not os.getenv('OPENAI_API_KEY'):
        raise SystemExit('Set OPENAI_API_KEY to run the LLM judge. No judge results are fabricated by this repo.')
    client=OpenAI(); df=pd.read_csv(args.input).fillna('')
    scores=[]
    rubric='Score each 1-5: relevance, groundedness, helpfulness, accuracy, tone. Groundedness means the reply does not invent facts beyond the evidence. Return JSON only.'
    for _,r in df.iterrows():
        prompt=f"{rubric}\nCustomer: {r.customer_text}\nEvidence: {r.evidence_text}\nDraft: {r.draft_reply}"
        resp=client.responses.create(model=os.getenv('OPENAI_JUDGE_MODEL','gpt-5-mini'),input=prompt)
        txt=resp.output_text.strip()
        try: scores.append(json.loads(txt))
        except Exception: scores.append({'raw':txt})
    out={'n':len(df),'scores':scores}
    os.makedirs(os.path.dirname(args.output),exist_ok=True)
    json.dump(out,open(args.output,'w'),indent=2)
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
