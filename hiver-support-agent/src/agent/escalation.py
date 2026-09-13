HIGH_RISK_TERMS=['hacked','unauthorized','fraud','counterfeit','illegal','stolen','identity','scam']

def decide_escalation(message, intent, confidence, evidence_score=0.0):
    t=message.lower()
    if any(x in t for x in HIGH_RISK_TERMS): return True, 'High-risk account/security or marketplace allegation.'
    if intent=='other_unclear': return True, 'Intent is unclear; insufficient context for safe automation.'
    if confidence < 0.55: return True, f'Low intent confidence ({confidence:.2f}).'
    if evidence_score < 0.15: return True, 'Weak historical evidence for a grounded reply.'
    return False, 'Routine intent with sufficient confidence and historical evidence.'
