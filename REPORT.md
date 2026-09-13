# Hiver SDE Intern — AmazonHelp AI Support Agent

## 1. Problem framing
The input is an incoming AmazonHelp customer tweet. The system predicts the customer's primary support intent, retrieves similar historical AmazonHelp interactions, drafts a response grounded in that evidence, and decides whether the case is safe to auto-handle or should be escalated.

The source data is tweet-level rather than case-level. We therefore use `in_response_to_tweet_id` and `response_tweet_id` to connect customer and support messages before treating an interaction as historical evidence. The public dataset documentation describes these fields as the response links between tweets. citeturn0search0turn0search1

## 2. Why AmazonHelp?
We compared brands using support volume, reconstructable conversation count, average conversation depth, and multi-turn rate. AmazonHelp provided a strong combination of scale and conversational depth, making it useful for learning historical support resolutions rather than only classifying isolated tweets. We intentionally keep the production scope to one brand so retrieval does not mix policies and workflows from unrelated companies.

## 3. Intent taxonomy
The initial taxonomy contains 14 operational classes: order status, delivery problem, missing/not received order, return, refund, payment/billing, cancellation, account/login, Prime, product problem, product information, promotion/discount, seller/marketplace, and other/unclear.

The 168-row review set is stratified at 12 examples per initial class. The final labels were semantically reviewed against the labeling guide for this time-constrained submission. Because an independent human annotator did not perform the review, the files record `ASSISTANT_SEMANTIC_REVIEWED`; this provenance limitation is explicitly disclosed.

## 4. Baselines and results
A majority-class baseline and TF-IDF + Logistic Regression were evaluated with 5-fold stratified cross-validation on the 168 reviewed examples.

| System | Accuracy | Macro-F1 |
|---|---:|---:|
| Majority baseline | 0.113 ± 0.014 | 0.015 ± 0.002 |
| TF-IDF + Logistic Regression | **0.434 ± 0.066** | **0.353 ± 0.075** |

The lexical model is a useful simple baseline: it substantially beats the majority classifier, but the macro-F1 variance shows that several intents remain difficult with short/noisy Twitter text.

The escalation gate was also evaluated against the reviewed escalation labels: accuracy 0.970, precision 1.000, recall 0.821, F1 0.902. These values are set-level diagnostics, not production estimates.

## 5. Proposed agent
The proposed agent is a staged pipeline:

`customer message → intent → historical retrieval → grounded draft → escalation gate`

The retrieval layer uses TF-IDF cosine similarity as the reproducible offline implementation. An LLM API can be added as the generation layer, with the retrieved historical responses passed as evidence. If evidence is weak or the case is high-risk, the escalation gate prevents automatic handling.

## 6. Evaluation plan
Final evaluation reports or supports:
- intent Accuracy and Macro-F1;
- retrieval Recall@5 and relevance on a hand-labelled subset;
- reply quality using relevance, groundedness, helpfulness, accuracy and tone scores from an LLM judge;
- escalation precision, recall and F1;
- agreement between LLM judge and human ratings on a held-out subset using Cohen's kappa or Spearman correlation.

The LLM judge harness is implemented in `scripts/judge_replies.py` and only runs when an API key is provided; it does not fabricate reply-quality scores. A held-out human-scored subset can be compared with judge scores using correlation/agreement metrics. The current submission therefore reports the intent and escalation diagnostics that can be reproduced offline and explicitly marks the reply-judge dependency.

## 7. Top failure modes to inspect
1. **Delivery vs missing-order confusion** — “delivery” is often mentioned in both classes; the distinction is whether the customer explicitly says the item was not received.
2. **Multi-intent tweets** — one tweet may contain a delivery complaint plus a refund request; a single-label taxonomy forces a primary intent.
3. **Short/ambiguous messages** — thanks, “help”, links, and follow-ups lack enough standalone context; these should bias toward `other_unclear` and escalation.
4. **Multilingual/mixed-language tweets** — the dataset contains messages in multiple languages, which can reduce lexical classifier quality.
5. **High-risk cases** — security, fraud, counterfeit, or account-compromise language can be lexically similar to routine support but should be escalated.

## 8. What is misleading about my headline number?
A single accuracy number can be misleading because the final golden set is small, intentionally stratified rather than naturally distributed, and subject to labeling ambiguity. A reply-quality LLM judge can also be more forgiving than a human support reviewer. Production performance would likely differ because real traffic has a different intent distribution and contains harder edge cases. Therefore the report must emphasize Macro-F1, per-intent results, retrieval evidence quality, escalation safety, and human-vs-LLM judge agreement rather than one aggregate score.

## 9. One-week next steps
- Human-verify and double-label the golden set.
- Add hard-negative retrieval examples from nearby intents.
- Replace lexical retrieval with sentence embeddings and compare Recall@K.
- Add confidence calibration for intent and retrieval scores.
- Expand escalation rules into a small risk policy with explicit test cases.
- Run human review of auto-generated replies and feed disagreement cases back into the taxonomy.
