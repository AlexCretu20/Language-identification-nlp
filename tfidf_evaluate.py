import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

from tfidf_model import TfidfLanguageClassifier


def bucket_length(text):
    l = len(text)
    if l < 20:
        return "<20"
    elif l < 50:
        return "20-50"
    else:
        return "50+"


def main():
    # ========================
    # LOAD DATA
    # ========================
    train_df = pd.read_csv("train.csv")
    test_df = pd.read_csv("test.csv")

    # CLEAN DATA 
    train_df = train_df.dropna(subset=["text"])
    test_df = test_df.dropna(subset=["text"])

    train_df["text"] = train_df["text"].astype(str)
    test_df["text"] = test_df["text"].astype(str)

    # PRECOMPUTE BUCKETS (for short text analysis)
    test_df["bucket"] = test_df["text"].apply(bucket_length)

    models = ["logreg", "svm"]
    results = []

    for m in models:
        print(f"\n========================")
        print(f"Running model: {m}")
        print(f"========================")

        # ========================
        # TRAIN MODEL
        # ========================
        model = TfidfLanguageClassifier(m)
        model.fit(train_df["text"], train_df["labels"])

        # ========================
        # PREDICT
        # ========================
        preds = model.predict(test_df["text"])

        # ========================
        # METRICS
        # ========================
        acc = accuracy_score(test_df["labels"], preds)
        f1 = f1_score(test_df["labels"], preds, average="macro")

        print("Accuracy:", acc)
        print("F1 (macro):", f1)
        print("\nClassification Report:\n")
        print(classification_report(test_df["labels"], preds))

        results.append({
            "model": m,
            "accuracy": acc,
            "f1_macro": f1
        })

        # ========================
        # CONFUSION MATRIX (only once)
        # ========================
        if m == "logreg":
            labels = sorted(test_df["labels"].unique())
            cm = confusion_matrix(test_df["labels"], preds, labels=labels)

            plt.figure(figsize=(12, 10))
            sns.heatmap(
                cm,
                cmap="Blues",
                xticklabels=labels,
                yticklabels=labels
            )

            plt.title("Confusion Matrix (LogReg)")
            plt.xlabel("Predicted")
            plt.ylabel("True")

            plt.tight_layout()
            plt.savefig("confusion_matrix.png")
            plt.close()

        # ========================
        # SHORT TEXT ANALYSIS
        # ========================
        print("\nShort text analysis:")

        for bucket in ["<20", "20-50", "50+"]:
            subset = test_df[test_df["bucket"] == bucket]

            if len(subset) == 0:
                continue

            preds_bucket = model.predict(subset["text"])

            acc_b = accuracy_score(subset["labels"], preds_bucket)
            f1_b = f1_score(subset["labels"], preds_bucket, average="macro")

            print(f"{bucket} -> Acc: {acc_b:.4f}, F1: {f1_b:.4f}")

    # ========================
    # SAVE RESULTS
    # ========================
    pd.DataFrame(results).to_csv("tfidf_results.csv", index=False)
    print("\nResults saved to tfidf_results.csv")


if __name__ == "__main__":
    main()