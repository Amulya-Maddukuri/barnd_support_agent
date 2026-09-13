"""Prepare a compact AmazonHelp interaction corpus from twcs.csv.
The full dataset is never committed; only a small derived artifact is written.
"""
import argparse, os
import pandas as pd

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', default='data/processed/amazonhelp_customer.csv')
    ap.add_argument('--max-rows', type=int, default=50000)
    args=ap.parse_args()
    # First collect IDs of AmazonHelp replies.
    support_ids=set()
    for ch in pd.read_csv(args.input, chunksize=200000, usecols=['tweet_id','author_id','inbound'],
                          dtype={'tweet_id':'int64','author_id':'string','inbound':'boolean'}):
        support_ids.update(ch.loc[(ch.author_id=='AmazonHelp') & (ch.inbound==False),'tweet_id'].tolist())
    out=[]
    for ch in pd.read_csv(args.input, chunksize=200000,
                          dtype={'tweet_id':'int64','author_id':'string','inbound':'boolean','created_at':'string','text':'string','response_tweet_id':'string','in_response_to_tweet_id':'float64'}):
        x=ch[(ch.inbound==True) & ch.in_response_to_tweet_id.isin(support_ids)].copy()
        if x.empty: continue
        x['text']=x.text.fillna('')
        x=x[x.text.str.len().between(10,1000)]
        out.append(x[['tweet_id','created_at','text','response_tweet_id','in_response_to_tweet_id']])
        if sum(len(z) for z in out)>=args.max_rows: break
    df=pd.concat(out,ignore_index=True).drop_duplicates('tweet_id').head(args.max_rows)
    os.makedirs(os.path.dirname(args.output),exist_ok=True); df.to_csv(args.output,index=False)
    print(f'wrote {len(df):,} AmazonHelp customer messages -> {args.output}')
if __name__=='__main__': main()
