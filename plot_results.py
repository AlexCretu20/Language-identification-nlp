import pandas as pd
import matplotlib.pyplot as plt


def plot_results(csv_file):
    df = pd.read_csv(csv_file)

    plt.figure()
    plt.bar(df["model"], df["accuracy"])
    plt.title("Accuracy Comparison")
    plt.xlabel("Model")
    plt.ylabel("Accuracy")
    plt.savefig("accuracy_plot.png")
    plt.close()

    plt.figure()
    plt.bar(df["model"], df["f1_macro"])
    plt.title("F1 Score Comparison")
    plt.xlabel("Model")
    plt.ylabel("F1 Macro")
    plt.savefig("f1_plot.png")
    plt.close()


if __name__ == "__main__":
    plot_results("tfidf_results.csv")