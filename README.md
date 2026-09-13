# Hiver SDE Intern - AI Support Agent

This project is an AI based customer support agent built using the Customer Support on Twitter dataset.

For this project I selected AmazonHelp as the brand. The agent takes a customer message, identifies the issue, finds similar historical support interactions, generates a reply based on that evidence, and decides whether the request should be handled automatically or escalated to a human.

1. Brand Selection

I selected AmazonHelp after comparing different support accounts in the dataset.

I mainly looked at the number of support interactions, conversation length and the percentage of multi-turn conversations.

AmazonHelp had around 82K reconstructable conversations, with an average of about 4.5 tweets per conversation and around 62% multi-turn conversations.

This made AmazonHelp a good choice because there is enough historical conversation data to use for retrieval.

2. Dataset

I used the Customer Support on Twitter dataset from Kaggle.

Dataset: thoughtvector/customer-support-on-twitter

The important columns used are tweet_id, author_id, inbound, created_at, text, response_tweet_id and in_response_to_tweet_id.

Each row represents a tweet. The response fields can be used to connect tweets and reconstruct conversations between customers and support accounts.

The complete dataset is not included in this repository because of its size.

3. Approach

The system works in four main stages.

Customer message -> Intent classification -> Historical retrieval -> Reply generation -> Escalation decision

The main idea is to use previous AmazonHelp interactions as evidence instead of generating a completely unsupported response.

4. Intent Categories

I created 14 support categories based on common issues in the AmazonHelp data.

Intent  and Description 
 order_status - Order or tracking status 
 delivery_problem - Late or problematic delivery 
 missing_or_not_received_order - Order or package was not received 
 return_request - Customer wants to return an item 
 refund_status - Customer is asking about a refund 
 payment_or_billing_problem - Payment, charge or billing issue 
 cancellation_request - Customer wants to cancel an order 
 account_or_login_problem - Login or account access issue 
 Amazon_Prime_problem - Prime membership or service issue 
 product_problem - Damaged, defective, wrong or non-working product 
 product_information - Product information, stock or availability 
 promotion_or_discount - Coupon, deal or discount issue 
 seller_or_marketplace_problem - Seller or marketplace issue 
 other_unclear - Unclear or unrelated request 

The detailed labeling rules are available in data/golden/LABELING_GUIDE.md.

5. Intent Classification

I used TF-IDF with word unigrams and bigrams followed by Logistic Regression.

I chose this approach because it is simple, fast and easy to reproduce.

The classifier is implemented in src/intents/classifier.py.

It returns the predicted intent along with a confidence score.

6. Intent Results

I evaluated the classifier using 5-fold stratified cross-validation on the 168-example evaluation set.

Majority baseline-Accuracy 11.32% and Macro-F1 1.45% 
TF-IDF + Logistic Regression-Accuracy 43.42% and Macro-F1 35.32% 

The classifier performs much better than the majority baseline, but the overall score is still not very high.

One reason is that some categories are very similar. For example, an order status question, a late delivery and a missing package can look almost the same when the customer gives very little context.

7. Historical Retrieval

After classification, the system searches historical AmazonHelp customer messages for similar examples.

The retrieval code is in src/retrieval/retrieve.py.

The current retriever uses TF-IDF and cosine similarity.

The retrieved examples are used as evidence while generating the response. This helps reduce the chance of making up policies, refund information or delivery promises.

8. Reply Generation

Reply generation is implemented in src/agent/generator.py.

If an OpenAI API key is available, the system can use the OpenAI Responses API to generate the reply.

The prompt tells the model to stay close to the retrieved evidence and not invent policies, dates or actions.

If no API key is available, the system uses a simple deterministic fallback response so that the project can still be run.

9. Escalation

The escalation logic is implemented in src/agent/escalation.py.

A request can be escalated when the system detects a risky situation, the intent is unclear, the classifier confidence is low or the retrieved evidence is weak.

Some examples of risky cases are account compromise, unauthorized activity, fraud, counterfeit products and scams.

The idea is to avoid automatically answering a case when the system is not confident enough.

10. Escalation Results

The escalation component was evaluated on the same 168-example set.

Accuracy 97.02% 
Precision 100.00% 
Recall 82.14% 
F1 90.20% 

There were 28 escalation-positive examples.

The high precision is useful because cases marked for escalation were correct in this evaluation set. However, the recall shows that some cases that should have been escalated were still missed.

11. Example

Example input:

My package says delivered but I never received it.

The system predicts:

missing_or_not_received_order

It then retrieves similar historical examples and uses them as evidence for the response.

If the confidence is low, the system can escalate the case instead of automatically handling it.

12. Evaluation Set

I created a 168-example evaluation set covering the 14 intent categories.

The files are available in data/golden/.

The main files are:

amazonhelp_golden_168.csv

amazonhelp_golden_168_review.csv

LABELING_GUIDE.md

The examples contain the customer message, intent label and escalation label.

The labels were semantically reviewed against the labeling guide, but they were not independently hand-labelled by another human annotator.

Because of this, I consider these results development evaluation results rather than a fully independent benchmark.

13. LLM Judge

The project also contains an LLM-as-judge script in scripts/judge_replies.py.

It is designed to score generated replies for relevance, groundedness, helpfulness, accuracy and tone.

The script requires an OpenAI API key.

I did not run the judge without an API credential, so I have not included fabricated judge scores in the results.

A future version should also compare the LLM judge scores with human ratings to measure judge-human agreement.

14. Main Failure Cases

The main problems I observed were:

1. Similar intents such as order status, delivery problem and missing order can be confused.

2. Very short messages such as "Help" or "Where is it?" do not contain enough information for reliable classification.

3. Product problems and return requests sometimes overlap.

4. TF-IDF retrieval can return examples that contain similar words but are not actually the best match.

5. The escalation system is currently rule based, so unusual wording can sometimes be missed.

The main improvement would be to use more conversation context and better semantic models.

15. What Is Misleading About the Headline Number?

The 97.02% escalation accuracy looks very good, but it should not be treated as the overall accuracy of the support agent.

The evaluation set has only 168 examples and only 28 escalation-positive examples. Also, the labels were not independently human-annotated.

The intent classifier itself has 43.42% accuracy, so there is still a lot of room for improvement.

The escalation result is therefore only a development result for one part of the system.

16. One Week Improvement Plan

If I had another week, I would focus on the following:

First, create a larger evaluation set with independent human annotation.

Second, compare the current TF-IDF classifier with sentence embeddings and transformer based models.

Third, improve retrieval using semantic embeddings and conversation-level context.

Fourth, build a dedicated risk classifier instead of relying mainly on keywords and thresholds.

Finally, run the LLM judge together with human evaluation and compare their scores.

17. How to Run

Install the required packages:


pip install -r requirements.txt


To prepare AmazonHelp data from the original dataset:


python scripts/prepare_data.py --input path/to/twcs.csv


Train the intent model:

python scripts/train_intent.py


Evaluate the classifier:


python scripts/evaluate_classifier.py


Evaluate escalation:


python scripts/evaluate_escalation.py


Run the agent with a sample message:


python scripts/run_agent.py --message "Where is my Amazon order?"


The output contains the predicted intent, confidence, retrieved evidence, generated reply and escalation decision.


18. Project Structure

hiver-support-agent/
├── README.md
├── REPORT.md
├── DECISION_LOG.md
├── requirements.txt
├── .env.example
├── .gitignore
├── data/
│   └── golden/
├── src/
│   ├── intents/
│   ├── retrieval/
│   ├── agent/
│   └── evaluation/
├── scripts/
└── outputs/

19. Important Design Decisions

Some of the main decisions I made were:

- Selecting AmazonHelp because of its conversation volume and multi-turn interactions.
- Keeping the intent taxonomy small enough to label consistently.
- Starting with TF-IDF and Logistic Regression as a simple baseline.
- Using historical retrieval to ground the generated response.
- Keeping a fallback response generator so the project can run without an API key.
- Escalating low-confidence and high-risk cases.
- Keeping the raw dataset outside the repository because of its size.
- Reporting limitations instead of presenting unavailable evaluation results.


20. Dataset Attribution

This project uses the Customer Support on Twitter dataset from Kaggle.

Dataset: thoughtvector/customer-support-on-twitter


21. Summary

This project implements a small retrieval-grounded customer support agent for AmazonHelp.

The current system uses a TF-IDF and Logistic Regression classifier, historical support retrieval, optional LLM based reply generation and a rule based escalation component.

The intent classifier achieved 43.42% accuracy and 35.32% Macro-F1 compared with 11.32% accuracy and 1.45% Macro-F1 for the majority baseline.

The escalation component achieved 97.02% accuracy, 100% precision, 82.14% recall and 90.20% F1 on the development evaluation set.

The main limitations are the small evaluation set, lack of independent human annotation, relatively simple retrieval and the fact that the LLM judge has not yet been run.

