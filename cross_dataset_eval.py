import pandas as pd
from datasets import load_dataset
from sklearn.metrics import accuracy_score, f1_score, classification_report

from bert_model import BertLanguageClassifier
from tfidf_model import TfidfLanguageClassifier
from shared_data import TARGET_LAN

SEP = "=" * 62


# ── load papluca test split ────────────────────────────────────
print("Loading papluca/language-identification …")
papluca = load_dataset("papluca/language-identification")
test_df = pd.DataFrame(papluca["test"])

# papluca may encode ClassLabel as integers — decode if needed
if pd.api.types.is_integer_dtype(test_df["labels"]):
    label_names = papluca["test"].features["labels"].names
    test_df["labels"] = test_df["labels"].map(lambda x: label_names[x])

test_df = test_df[test_df["labels"].isin(TARGET_LAN)].reset_index(drop=True)
test_df = test_df.dropna(subset=["text"])
test_df["text"] = test_df["text"].astype(str)

present  = sorted(test_df["labels"].unique())
excluded = [l for l in TARGET_LAN if l not in present]
print(f"Test rows after filter : {len(test_df)}")
print(f"Languages evaluated    : {present}")
print(f"Excluded (not in papluca): {excluded}")

gold = test_df["labels"]


# ── train TF-IDF on our train.csv ─────────────────────────────
print("\nTraining TF-IDF LogReg on train.csv …")
train_df = pd.read_csv("train.csv").dropna(subset=["text"])
train_df["text"] = train_df["text"].astype(str)
tfidf = TfidfLanguageClassifier("logreg")
tfidf.fit(train_df["text"], train_df["labels"])


# ── helper ────────────────────────────────────────────────────
def evaluate(name, preds, gold, labels):
    acc = accuracy_score(gold, preds)
    f1  = f1_score(gold, preds, average="macro", labels=labels)
    print(f"\n{SEP}")
    print(f"  {name}")
    print(SEP)
    print(classification_report(gold, preds, labels=labels, zero_division=0))
    print(f"  Accuracy : {acc:.4f}")
    print(f"  Macro F1 : {f1:.4f}")
    return acc, f1


# ── BERT ──────────────────────────────────────────────────────
print("\nRunning BERT inference on papluca test split …")
bert = BertLanguageClassifier()
bert_preds = bert.predict(test_df["text"])
bert_acc, bert_f1 = evaluate(
    "BERT  (papluca/xlm-roberta-base-language-detection)",
    bert_preds, gold, present,
)

# ── TF-IDF ────────────────────────────────────────────────────
print("\nRunning TF-IDF LogReg on papluca test split …")
tfidf_preds = tfidf.predict(test_df["text"])
tfidf_acc, tfidf_f1 = evaluate(
    "TF-IDF LogReg  (trained on our train.csv)",
    tfidf_preds, gold, present,
)


# ── side-by-side summary ──────────────────────────────────────
print(f"\n{SEP}")
print("  CROSS-DATASET SUMMARY")
print(SEP)
print(f"  Dataset  : papluca/language-identification  (test split)")
print(f"  Evaluated languages ({len(present)}/{len(TARGET_LAN)}): {present}")
print(f"  Excluded : {excluded}  — not present in papluca")
print(f"\n  {'Model':<35} {'Accuracy':>9} {'Macro F1':>9}")
print(f"  {'-'*35} {'-'*9} {'-'*9}")
print(f"  {'BERT (in-distribution)':<35} {bert_acc:>9.4f} {bert_f1:>9.4f}")
print(f"  {'TF-IDF LogReg (cross-dataset)':<35} {tfidf_acc:>9.4f} {tfidf_f1:>9.4f}")
print(SEP)


# ── save ──────────────────────────────────────────────────────
results = pd.DataFrame([
    {"model": "BERT",          "dataset": "papluca", "accuracy": bert_acc,  "f1_macro": bert_f1},
    {"model": "TF-IDF LogReg", "dataset": "papluca", "accuracy": tfidf_acc, "f1_macro": tfidf_f1},
])
results.to_csv("cross_dataset_results.csv", index=False)
print(f"\nSaved -> cross_dataset_results.csv")
