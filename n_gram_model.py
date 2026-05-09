import math
import pandas as pd
from collections import Counter, defaultdict
from sklearn.metrics import accuracy_score, classification_report

## pregatire n grame
def get_ngram(text, n = 3):
    piese = []

    for i in range(len(text) - n + 1):
        piese.append(text[i : i + n])

    return piese


def train(text_train, labels_train, n = 3):

    draws = defaultdict(Counter)
    count_piese_per_draw = defaultdict(int)
    vocabulary = set()
    lang = list(set(labels_train))

    for text, lan in zip(text_train, labels_train):
        pieces = get_ngram(text,n)

        draws[lan].update(pieces)
        count_piese_per_draw[lan] += len(pieces)

        vocabulary.update(pieces)

    print(f"we have {len(vocabulary)} words")

    return  draws, count_piese_per_draw, vocabulary, lang

def identify_language(text, draws, count_piese_per_draw, vocabulary, lang, n = 3):

    new_pieses = get_ngram(text, n)

    best_score = -float('inf')
    identify_lang = None
    count_draw = len(vocabulary)

    for lg in lang:
        lang_score = 0.0
        numitor = count_piese_per_draw[lg] + count_draw

        for p in new_pieses:
            aparitii = draws[lg].get(p, 0)

            prob = (aparitii + 1) / numitor
            lang_score += math.log(prob)

        if lang_score > best_score:
            best_score = lang_score
            identify_lang = lg

    return identify_lang

def test_model(text_test, label_text, draws, count_piese_per_draw, vocabulary, langs, n = 3 ):

    predictions = []
    for text in text_test:
        rez = identify_language(text, draws, count_piese_per_draw, vocabulary, langs, n)
        predictions.append(rez)

    accuracy = accuracy_score(label_text, predictions)
    raport  = classification_report(label_text, predictions, output_dict = True)

    return accuracy, raport, predictions

if __name__ == "__main__":
    try:
        table_train = pd.read_csv("train.csv").dropna(subset=['text', 'labels'])
        table_test = pd.read_csv("test.csv").dropna(subset=['text', 'labels'])
        table_dev = pd.read_csv("dev.csv").dropna(subset=['text', 'labels'])

        texts_train = table_train['text'].tolist()
        lables_train = table_train['labels'].tolist()

        texts_dev = table_dev['text'].tolist()
        lables_dev = table_dev['labels'].tolist()

        texts_test = table_test['text'].tolist()
        lables_test = table_test['labels'].tolist()

        # caut cel bun n
        val_n = [2,3,4]
        best_n = 3
        best_accuracy = 0

        for n in val_n:
            print(f"Testing n {n}")

            draws, count_piese_per_draw, vocabulary, langs = train(texts_train, lables_train, n = n)
            acc_dev, a, b = test_model(texts_dev, lables_dev, draws, count_piese_per_draw, vocabulary, langs, n = n)

            print(f"Score on dev :{acc_dev * 100:.2f}")

            if acc_dev > best_accuracy:
                best_accuracy = acc_dev
                best_n = n

        print(f"Best n is : {best_n}")

        # folosim n gasit ca sa obtinem cel mai bune rezultate
        draws, count_piese_per_draw, vocabulary, langs = train(texts_train, lables_train, n=best_n)

        acc_train, raport_train, predictions_train = test_model(texts_test, lables_test, draws, count_piese_per_draw, vocabulary, langs, n = best_n )

        # print(raport_train)

        # salvam rezultatele intr-un csv
        rez = pd.DataFrame({
            'text': texts_test,
            'real language': lables_test,
            'identified language': predictions_train
        })

        rez.to_csv("result.csv", index = False)

        raport = pd.DataFrame(raport_train).transpose()
        raport.to_csv("raport.csv", index = True)

    except FileNotFoundError:
        print("File not found. ")













