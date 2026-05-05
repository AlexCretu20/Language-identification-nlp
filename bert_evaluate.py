import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, classification_report

from bert_model import BertLanguageClassifier

def main():
    test_df = pd.read_csv("test.csv")
    test_df = test_df.dropna(subset=["text"])
    test_df["text"] = test_df["text"].astype(str)

    model = BertLanguageClassifier()

    preds = []
    for t in test_df["text"]:
        preds.append(model.predict_one(t))

    acc = accuracy_score(test_df["labels"], preds)
    f1 = f1_score(test_df["labels"], preds, average="macro")

    print("Accuracy:", acc)
    print("F1:", f1)
    print("\nReport:\n")
    print(classification_report(test_df["labels"], preds))

    # save results
    pd.DataFrame({
        "accuracy": [acc],
        "f1_macro": [f1]
    }).to_csv("bert_results.csv", index=False)

if __name__ == "__main__":
    main()