"""
Per-language accuracy for N-gram, TF-IDF (logreg + svm), and BERT.
"""
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score

from n_gram_model import train, test_model
from tfidf_model import TfidfLanguageClassifier
from bert_model import BertLanguageClassifier

DIVIDER = "=" * 60


def per_lang_accuracy(report_dict, labels):
    print(f"{'Language':<12} {'Accuracy (precision)':<25} {'Recall':<10} {'F1':<10} {'Support'}")
    print("-" * 65)
    for lang in sorted(labels):
        row = report_dict.get(lang, {})
        print(
            f"{lang:<12} {row.get('precision', 0):.4f}{'':>19} "
            f"{row.get('recall', 0):.4f}     "
            f"{row.get('f1-score', 0):.4f}     "
            f"{int(row.get('support', 0))}"
        )


def main():
    train_df = pd.read_csv("train.csv").dropna(subset=["text", "labels"])
    test_df  = pd.read_csv("test.csv").dropna(subset=["text", "labels"])
    dev_df   = pd.read_csv("dev.csv").dropna(subset=["text", "labels"])

    train_df["text"] = train_df["text"].astype(str)
    test_df["text"]  = test_df["text"].astype(str)
    dev_df["text"]   = dev_df["text"].astype(str)

    labels = sorted(test_df["labels"].unique())

    # ── N-gram ──────────────────────────────────────────────────────────
    print(f"\n{DIVIDER}")
    print("N-GRAM MODEL (selecting best n on dev set)")
    print(DIVIDER)

    best_n, best_acc = 3, 0.0
    for n in [2, 3, 4]:
        draws, counts, vocab, langs = train(train_df["text"].tolist(), train_df["labels"].tolist(), n=n)
        acc_dev, _, _ = test_model(dev_df["text"].tolist(), dev_df["labels"].tolist(), draws, counts, vocab, langs, n=n)
        print(f"  n={n}  dev acc={acc_dev:.4f}")
        if acc_dev > best_acc:
            best_acc, best_n = acc_dev, n

    print(f"  -> Best n={best_n}")
    draws, counts, vocab, langs = train(train_df["text"].tolist(), train_df["labels"].tolist(), n=best_n)
    acc, report_dict, _ = test_model(test_df["text"].tolist(), test_df["labels"].tolist(), draws, counts, vocab, langs, n=best_n)
    print(f"\nOverall accuracy: {acc:.4f}")
    per_lang_accuracy(report_dict, labels)

    # ── TF-IDF ──────────────────────────────────────────────────────────
    for variant in ["logreg", "svm"]:
        print(f"\n{DIVIDER}")
        print(f"TF-IDF  ({variant.upper()})")
        print(DIVIDER)

        clf = TfidfLanguageClassifier(variant)
        clf.fit(train_df["text"], train_df["labels"])
        preds = clf.predict(test_df["text"])

        report = classification_report(test_df["labels"], preds, labels=labels, output_dict=True)
        acc = report["accuracy"]
        print(f"\nOverall accuracy: {acc:.4f}")
        per_lang_accuracy(report, labels)

    # ── BERT ─────────────────────────────────────────────────────────────
    print(f"\n{DIVIDER}")
    print("BERT  (xlm-roberta-base-language-detection)")
    print(DIVIDER)

    bert = BertLanguageClassifier()
    preds = bert.predict(test_df["text"].tolist())

    acc = accuracy_score(test_df["labels"], preds)
    report = classification_report(test_df["labels"], preds, labels=labels, output_dict=True, zero_division=0)
    print(f"\nOverall accuracy: {acc:.4f}")
    per_lang_accuracy(report, labels)


if __name__ == "__main__":
    main()
