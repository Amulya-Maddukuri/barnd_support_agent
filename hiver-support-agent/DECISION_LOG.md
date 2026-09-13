# Decision Log

1. **Single brand: AmazonHelp** — enough scale and conversation depth while avoiding cross-brand policy leakage.
2. **Conversation reconstruction** — a CSV row is a tweet, not a support case; response-link fields are required to recover interaction context.
3. **Customer-first intent labels** — classify what the customer is trying to achieve, not the wording of the agent response.
4. **14 initial intents** — broad operational categories avoid sparse classes while preserving distinct workflows.
5. **Keep `other_unclear`** — uncertainty is a real system state and should support escalation instead of forced classification.
6. **TF-IDF + Logistic Regression baseline** — fast, interpretable and reproducible within the take-home time budget.
7. **Retrieval before generation** — historical AmazonHelp responses are the grounding source; generation should not invent policy.
8. **Brand-restricted retrieval** — similar language across brands does not imply identical policy or workflow.
9. **Escalation as a separate gate** — intent confidence alone is insufficient for high-risk cases.
10. **High-risk lexical triggers** — account compromise, fraud and counterfeit allegations are safer to route to humans even when the intent classifier is confident.
11. **Stratified golden-set sampling** — ensures every operational intent has evaluation coverage; natural traffic frequency is reported separately because stratification changes the distribution.
12. **Human verification required** — assistant-proposed labels are used to accelerate annotation but are never presented as hand labels until a human reviewer confirms them.
13. **Offline fallback** — the core classifier/retriever runs without an external LLM so the evaluator can reproduce the pipeline; LLM generation is an optional enhancement.
14. **No fabricated headline results** — development/silver metrics are clearly separated from final golden-set metrics.
