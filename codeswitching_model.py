import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForTokenClassification


def load_model(path="codeswitch_model"):
    p = Path(path).resolve()
    print(f"Loading model from {p} ...")
    tokenizer = AutoTokenizer.from_pretrained(str(p), local_files_only=True)
    model = AutoModelForTokenClassification.from_pretrained(str(p), local_files_only=True)
    model.eval()
    print("Model loaded!")
    return model, tokenizer


def predict(sentence, model, tokenizer):
    words = sentence.split()
    encoding = tokenizer(
        words,
        is_split_into_words=True,
        return_tensors="pt",
        truncation=True,
    )
    word_ids = tokenizer(
        words,
        is_split_into_words=True,
        truncation=True,
    ).word_ids(batch_index=0)

    with torch.no_grad():
        logits = model(**encoding).logits

    preds = logits.argmax(dim=-1)[0].tolist()
    lbl_map = model.config.id2label

    seen, result = set(), []
    for wid, pid in zip(word_ids, preds):
        if wid is None or wid in seen:
            continue
        seen.add(wid)
        raw = lbl_map[pid]
        label = "RO" if raw == "lang1" else "EN" if raw == "lang2" else "OTHER"
        result.append((words[wid], label))
    return result


class CodeSwitchingDetector:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def load(self, path="codeswitch_model"):
        self.model, self.tokenizer = load_model(path)

    def predict_tokens(self, sentence):
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded. Call load() first.")
        return predict(sentence, self.model, self.tokenizer)