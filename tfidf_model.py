from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC


class TfidfLanguageClassifier:
    def __init__(self, model_type="logreg"):
        self.vectorizer = TfidfVectorizer(
            analyzer='char',
            ngram_range=(2, 4)
        )

        if model_type == "logreg":
            self.model = LogisticRegression(max_iter=1000)
        else:
            self.model = LinearSVC()

    def fit(self, texts, labels):
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def predict(self, texts):
        X = self.vectorizer.transform(texts)
        return self.model.predict(X)

    def predict_one(self, text):
        return self.predict([text])[0]