from sklearn.metrics import accuracy_score, f1_score, classification_report

def intent_metrics(y_true,y_pred):
    return {'accuracy':float(accuracy_score(y_true,y_pred)), 'macro_f1':float(f1_score(y_true,y_pred,average='macro'))}
