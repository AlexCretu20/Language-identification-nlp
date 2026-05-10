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
# LOAD CODE-SWITCHING MODEL
# =========================
try:
    from codeswitching_model import CodeSwitchingDetector
    import os
    if os.path.exists("codeswitch_model"):
        print("Loading code-switch model...")
        cs_detector = CodeSwitchingDetector()
        cs_detector.load("codeswitch_model")
        print("Code-switching model ready!")
    else:
        cs_detector = None
        print("WARNING: codeswitch_model/ folder not found. Run Colab notebook first.")
except Exception as e:
    cs_detector = None
    print(f"WARNING: Code-switching model not loaded ({e}). Run Colab notebook first.")
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
# GRADIO INTERFACES
# =========================
lang_interface = gr.Interface(
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


def detect_codeswitching(text):
    if cs_detector is None:
        return [("⚠️ cs_model/ not found. Run Colab notebook first.", "OTHER")]
    return cs_detector.predict_tokens(text)


cs_interface = gr.Interface(
    fn=detect_codeswitching,
    inputs=gr.Textbox(lines=2, placeholder="Ce faci bro how are you..."),
    outputs=gr.HighlightedText(color_map={"EN": "blue", "RO": "green", "OTHER": "gray"}),
    examples=[
        ["Ce faci bro how are you"],
        ["Merg la gym dupa work"],
        ["Deadline-ul e maine si n-am facut nimic"],
        ["Am dat update la laptop si acum crapa tot"],
        ["Bro seriously nu mai pot cu oamenii astia"],
    ],
    title="Code-Switching Detector",
    description="Detecteaza limba fiecarui cuvant: 🟢 Romana | 🔵 Engleza",
)

app = gr.TabbedInterface(
    [lang_interface, cs_interface],
    ["Language Identification", "Code-Switching"],
)

app.launch()