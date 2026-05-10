import csv
import os
from collections import defaultdict
from sklearn.metrics import classification_report
from codeswitching_model import CodeSwitchingDetector

HERE = os.path.dirname(os.path.abspath(__file__))

detector = CodeSwitchingDetector.__new__(CodeSwitchingDetector)
detector.load("cs_model")

# group romgleza.csv by sentence_id
groups = defaultdict(list)
with open(os.path.join(HERE, "romgleza.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        groups[int(row["sentence_id"])].append(row)

all_gold, all_pred, result_rows = [], [], []

for sid in sorted(groups):
    rows     = groups[sid]
    sentence = " ".join(r["token"] for r in rows)
    gold     = [r["label"] for r in rows]
    preds    = detector.predict_tokens(sentence)
    pred     = [lbl for _, lbl in preds]

    n = min(len(gold), len(pred))
    gold, pred = gold[:n], pred[:n]
    tokens = [r["token"] for r in rows[:n]]

    # print sentence with inline token/label pairs
    inline = " ".join(f"{t} [{p}/{g}]" for t, p, g in zip(tokens, pred, gold))
    print(f"\n[{sid}] {sentence}")
    print(f"     {inline}")

    all_gold.extend(gold)
    all_pred.extend(pred)
    for tok, g, p in zip(tokens, gold, pred):
        result_rows.append([sid, tok, g, p])

# overall metrics
print("\n" + "=" * 60)
print(classification_report(all_gold, all_pred, zero_division=0))

# save csv
out = os.path.join(HERE, "cs_results.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["sentence_id", "token", "gold_label", "predicted_label"])
    w.writerows(result_rows)
print(f"Saved → {out}")
