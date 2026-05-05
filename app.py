import gradio as gr
import pandas as pd

from tfidf_model import TfidfLanguageClassifier
from bert_model import BertLanguageClassifier
from shared_data import clean_data

# =========================
# LOAD & TRAIN TF-IDF MODEL
# =========================
print("Loading and training TF-IDF model...")

train_df = pd.read_csv("train.csv")
train_df = train_df.dropna(subset=["text"])
train_df["text"] = train_df["text"].astype(str)

tfidf_model = TfidfLanguageClassifier("logreg")
tfidf_model.fit(train_df["text"], train_df["labels"])

print("TF-IDF model ready!")

# =========================
# LOAD BERT MODEL
# =========================
print("Loading BERT model...")
bert_model = BertLanguageClassifier()
print("BERT ready!")

# =========================
# PREDICTION FUNCTION
# =========================
def identify_language(text):
    text = clean_data(text)

    tfidf_pred = tfidf_model.predict_one(text)
    bert_pred, bert_score = bert_model.predict_one_with_score(text)

    #  Confidence interpretation
    if bert_score > 0.8:
        conf_status = "High confidence"
    elif bert_score > 0.5:
        conf_status = " Medium confidence"
    else:
        conf_status = " Low confidence"

    #  Disagreement detection
    if tfidf_pred == bert_pred:
        agreement = " Models agree"
    else:
        agreement = " Models disagree"

    #  Pretty output
    result = f"""
###  Results

- **TF-IDF Prediction:** `{tfidf_pred}`
- **BERT Prediction:** `{bert_pred}`
- **BERT Confidence:** `{bert_score}` → {conf_status}

---

###  Model Comparison
{agreement}
"""

    return result


# =========================
# EXAMPLES (pentru demo)
# =========================
examples = [
    ["Hello how are you"],
    ["Ce faci boss"],
    ["Aceasta este o propoziție scrisă corect în limba română"],
    ["salutatre acest text este in romana"],
    ["ce faci bro how are you"]
]

# =========================
# GRADIO APP
# =========================
app = gr.Interface(
    fn=identify_language,
    inputs=gr.Textbox(lines=4, placeholder="Enter text here..."),
    outputs=gr.Markdown(),
    examples=examples,
    title=" Language Identification Demo",
    description="""
Compare **TF-IDF (classical ML)** vs **BERT (deep learning)**.

 Try:
- short text
- informal text
- mixed languages (romgleză)
"""
)

app.launch()