from bert_model import BertLanguageClassifier

model = BertLanguageClassifier()

print(model.predict_one("Hello how are you"))
print(model.predict_one("Ce faci frate"))