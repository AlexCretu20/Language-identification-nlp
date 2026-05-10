import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, classification_report

from bert_model import BertLanguageClassifier
from shared_data import TARGET_LAN

def main():
    test_df = pd.read_csv("test.csv")
    test_df = test_df.dropna(subset=["text"])
    test_df["text"] = test_df["text"].astype(str)

    model = BertLanguageClassifier()

    preds = []
    for t in test_df["text"]:
        preds.append(model.predict_one(t))

    acc = accuracy_score(test_df["labels"], preds)
    # restrict macro F1 to our 13 target labels so unsupported-language
    # predictions (bg, el, hi …) don't inflate the denominator
    gold_labels = sorted(test_df["labels"].unique())
    f1 = f1_score(test_df["labels"], preds, average="macro", labels=gold_labels)

    print("Accuracy:", acc)
    print("F1:", f1)
    print("\nReport (target labels only):\n")
    print(classification_report(test_df["labels"], preds, labels=gold_labels))

    # save results
    pd.DataFrame({
        "accuracy": [acc],
        "f1_macro": [f1]
    }).to_csv("bert_results.csv", index=False)

if __name__ == "__main__":
    main()