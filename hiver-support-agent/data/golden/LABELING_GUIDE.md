# AmazonHelp Golden-Set Labeling Guide

The file `amazonhelp_golden_168_review.csv` contains 168 AmazonHelp customer messages sampled across 14 candidate intents. `proposed_intent` is **assistant-proposed only**. A row becomes part of the final golden set only after a human reviewer sets `final_intent` and `escalation_gold`.

## Labels
- `order_status`: tracking/status/location of an order when the main problem is not a failed delivery.
- `delivery_problem`: late, failed, mishandled, or problematic delivery process.
- `missing_or_not_received_order`: customer explicitly says package was not received/missing, including “marked delivered but not received.”
- `return_request`: how to return, return label/window/pickup.
- `refund_status`: refund requested, pending, missing, wrong refund destination, or refund outcome.
- `payment_or_billing_problem`: charge, payment method, billing, invoice, or payment failure.
- `cancellation_request`: explicit request to cancel an order/service.
- `account_or_login_problem`: login, password, account access, changed email, compromised account.
- `Amazon_Prime_problem`: Prime membership, Prime delivery/benefits, or Prime Video.
- `product_problem`: damaged, defective, broken, wrong item, missing component, not working.
- `product_information`: availability, specifications, sizing, stock, or general product information.
- `promotion_or_discount`: coupon, promotion, deal, discount, price matching.
- `seller_or_marketplace_problem`: seller conduct, marketplace, counterfeit/fraudulent seller/product allegations.
- `other_unclear`: insufficient context, social chatter, thanks, or issue not covered above.

## Escalation labels
Set `escalation_gold` to `yes` when a human should review because of security/fraud/counterfeit allegations, account compromise, legal/safety concerns, severe ambiguity, or insufficient evidence. Use `no` for routine, well-understood cases where historical evidence is adequate.

## Fast review protocol
1. Read `customer_text`.
2. Accept `proposed_intent` if it matches the customer's primary need; otherwise replace `final_intent`.
3. Set `escalation_gold` to `yes` for high-risk/unclear cases.
4. Add a short note only when the decision is non-obvious.
5. Change `review_status` to `HUMAN_VERIFIED` after reviewing the row.

Do not describe this file as hand-labelled until the review is complete.
