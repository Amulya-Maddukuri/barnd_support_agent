import os


def draft_reply(customer_message, intent, evidence):
    """Generate a grounded reply.

    Uses an LLM when OPENAI_API_KEY is configured; otherwise falls back to a
    deterministic template so the pipeline remains runnable offline.
    """
    if not evidence:
        return 'Thanks for reaching out. I’m sorry you’re having trouble. A support specialist should review this case and help with the next step.'
    if os.getenv('OPENAI_API_KEY'):
        try:
            from openai import OpenAI
            client=OpenAI()
            evidence_text='\n\n'.join(f"Historical case {i+1}: {e['text']}" for i,e in enumerate(evidence[:3]))
            prompt=("You are an Amazon customer-support drafting assistant. Draft a concise, safe reply "
                    "grounded only in the historical examples below. Do not invent policies, refunds, "
                    "dates, guarantees, or actions. If the evidence is insufficient, ask for the minimum "
                    "missing information or recommend human review.\n\n"
                    f"Customer message: {customer_message}\nIntent: {intent}\n\nEvidence:\n{evidence_text}")
            r=client.responses.create(model=os.getenv('OPENAI_MODEL','gpt-5-mini'),input=prompt)
            return r.output_text.strip()
        except Exception:
            pass
    return (f"I’m sorry you’re dealing with this. Based on similar Amazon support cases, this looks like a "
            f"{intent.replace('_',' ')} issue. Please share the relevant order or account details through "
            "the official support channel so the team can verify the case and take the appropriate next step.")
