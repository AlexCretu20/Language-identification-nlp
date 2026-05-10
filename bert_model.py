from transformers import pipeline
from shared_data import clean_data

class BertLanguageClassifier:
    def __init__(self):
        self.model = pipeline(
            "text-classification",
            model="papluca/xlm-roberta-base-language-detection"
        )

    def predict_one(self, text):
        text = clean_data(text)

        result = self.model(text, truncation=True, max_length=512)[0]

        # label vine gen "en", "ro"
        return result["label"]

    def predict(self, texts):
        return [self.predict_one(t) for t in texts]

    def predict_one_with_score(self, text):
        text = clean_data(text)
        result = self.model(text, truncation=True, max_length=512)[0]
        return result["label"], round(result["score"], 3)