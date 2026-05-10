import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
from bert_model import BertLanguageClassifier

test_df = pd.read_csv("test.csv").dropna(subset=["text", "labels"])
test_df["text"] = test_df["text"].astype(str)
labels = sorted(test_df["labels"].unique())

bert = BertLanguageClassifier()
preds = bert.predict(test_df["text"].tolist())

acc = accuracy_score(test_df["labels"], preds)
report = classification_report(test_df["labels"], preds, labels=labels, output_dict=True, zero_division=0)

print(f"\nBERT (xlm-roberta-base-language-detection)")
print(f"Overall accuracy: {acc:.4f}\n")
print(f"{'Language':<12} {'Precision':<12} {'Recall':<10} {'F1':<10} {'Support'}")
print("-" * 55)
for lang in sorted(labels):
    row = report.get(lang, {})
    print(
        f"{lang:<12} {row.get('precision', 0):.4f}       "
        f"{row.get('recall', 0):.4f}     "
        f"{row.get('f1-score', 0):.4f}     "
        f"{int(row.get('support', 0))}"
    )
