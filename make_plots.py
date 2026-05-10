import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report

from shared_data import TARGET_LAN
from tfidf_model import TfidfLanguageClassifier
from bert_model import BertLanguageClassifier
from n_gram_model import train as ngram_train, identify_language as ngram_predict

os.makedirs("figures", exist_ok=True)

MODELS       = ["N-gram", "TF-IDF LogReg", "TF-IDF SVM", "BERT"]
COLORS       = ["#4878d0", "#ee854a", "#6acc65", "#d65f5f"]
BUCKETS      = ["<20", "20-50", "50+"]
BUCKET_XLABELS = ["< 20 chars", "20–50 chars", "50+ chars"]
BAR_OFFSETS  = [-1.5, -0.5, 0.5, 1.5]


def bucket(text):
    n = len(text)
    if n < 20:  return "<20"
    if n < 50:  return "20-50"
    return "50+"


def style_ax(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, color="#e0e0e0", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


# ── load data ──────────────────────────────────────────────────────────
print("Loading train / test data …")
train_df = pd.read_csv("train.csv").dropna(subset=["text"])
test_df  = pd.read_csv("test.csv").dropna(subset=["text"])
train_df["text"] = train_df["text"].astype(str)
test_df["text"]  = test_df["text"].astype(str)
test_df["bucket"] = test_df["text"].apply(bucket)

# ── train and predict all models ───────────────────────────────────────
print("Training N-gram (n=3) …")
draws, counts, vocab, langs = ngram_train(
    train_df["text"].tolist(), train_df["labels"].tolist(), n=3
)
test_df["ngram_pred"] = [
    ngram_predict(t, draws, counts, vocab, langs, n=3)
    for t in test_df["text"]
]

print("Training TF-IDF LogReg …")
logreg = TfidfLanguageClassifier("logreg")
logreg.fit(train_df["text"], train_df["labels"])
test_df["logreg_pred"] = logreg.predict(test_df["text"])

print("Training TF-IDF SVM …")
svm = TfidfLanguageClassifier("svm")
svm.fit(train_df["text"], train_df["labels"])
test_df["svm_pred"] = svm.predict(test_df["text"])

print("Running BERT inference (this takes a while) …")
bert = BertLanguageClassifier()
test_df["bert_pred"] = bert.predict(test_df["text"])

# ── build classification reports once (shared by all figures) ──────────
PRED_COLS = ["ngram_pred", "logreg_pred", "svm_pred", "bert_pred"]
gold = test_df["labels"]

reports = {
    name: classification_report(gold, test_df[col], output_dict=True, zero_division=0)
    for name, col in zip(MODELS, PRED_COLS)
}

# ── Figure 1 : overall accuracy + macro F1 ────────────────────────────
accs = [accuracy_score(gold, test_df[col]) for col in PRED_COLS]
f1s  = [reports[name]["macro avg"]["f1-score"] for name in MODELS]

x, w = np.arange(len(MODELS)), 0.35
fig, ax = plt.subplots(figsize=(8, 5))
bars_acc = ax.bar(x - w / 2, accs, w, label="Accuracy", color="#4878d0", zorder=3)
bars_f1  = ax.bar(x + w / 2, f1s,  w, label="Macro F1", color="#ee854a", zorder=3)
for bar in bars_acc:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
            f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=8)
for bar in bars_f1:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
            f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels(MODELS)
ax.set_ylim(0, 1.12)
ax.set_ylabel("Score")
ax.set_title("Overall Model Comparison", fontsize=13, pad=12)
ax.legend(framealpha=0.3)
style_ax(ax)
plt.tight_layout()
plt.savefig("figures/model_comparison.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved figures/model_comparison.png")

# ── Figure 2 : per-language F1 ────────────────────────────────────────
lang_f1s = {
    name: [reports[name].get(lang, {}).get("f1-score", 0.0) for lang in TARGET_LAN]
    for name in MODELS
}

x, w = np.arange(len(TARGET_LAN)), 0.18
fig, ax = plt.subplots(figsize=(14, 5))
for name, offset, color in zip(MODELS, BAR_OFFSETS, COLORS):
    ax.bar(x + offset * w, lang_f1s[name], w, label=name, color=color, zorder=3)
ax.set_xticks(x)
ax.set_xticklabels(TARGET_LAN)
ax.set_ylim(0, 1.12)
ax.set_ylabel("F1 Score")
ax.set_title("Per-Language F1 Score by Model", fontsize=13, pad=12)
ax.legend(framealpha=0.3)
style_ax(ax)
plt.tight_layout()
plt.savefig("figures/per_language_f1.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved figures/per_language_f1.png")

# ── Figure 3 : accuracy by text-length bucket ─────────────────────────
bucket_accs = {
    name: [
        accuracy_score(sub["labels"], sub[col])
        if len(sub := test_df[test_df["bucket"] == b]) > 0 else 0.0
        for b in BUCKETS
    ]
    for name, col in zip(MODELS, PRED_COLS)
}

x, w = np.arange(len(BUCKETS)), 0.18
fig, ax = plt.subplots(figsize=(8, 5))
for name, offset, color in zip(MODELS, BAR_OFFSETS, COLORS):
    ax.bar(x + offset * w, bucket_accs[name], w, label=name, color=color, zorder=3)
ax.set_xticks(x)
ax.set_xticklabels(BUCKET_XLABELS)
ax.set_ylim(0, 1.12)
ax.set_ylabel("Accuracy")
ax.set_title("Accuracy by Text Length Bucket", fontsize=13, pad=12)
ax.legend(framealpha=0.3)
style_ax(ax)
plt.tight_layout()
plt.savefig("figures/short_text_analysis.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved figures/short_text_analysis.png")
