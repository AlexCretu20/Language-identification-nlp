import pandas as pd
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from shared_data import TARGET_LAN, LANG_MAP,  clean_data


def get_wili():

    wili = load_dataset("wili_2018")
    df_wili = pd.concat([
        pd.DataFrame(wili['train']),
        pd.DataFrame(wili['test'])],
        ignore_index = True)

    df_wili = df_wili.rename(columns={'sentence': 'text', 'label': 'labels'})
    df_wili['labels'] = df_wili['labels'].map(LANG_MAP)
    df_wili_final = df_wili[df_wili['labels'].isin(TARGET_LAN)].copy()

    return  df_wili_final

def get_tatoeba():
    # use an preproceset dataset for
    papluca = load_dataset("papluca/language-identification")

    df_papluca = pd.concat([
        pd.DataFrame(papluca['train']),
        pd.DataFrame(papluca['validation']),
        pd.DataFrame(papluca['test'])
    ], ignore_index = True)

    lang = [l for l in TARGET_LAN if l not in  ['ro', 'hu']]
    df_papluca_final = df_papluca[df_papluca['labels'].isin(lang)].copy()

    opus_ro = load_dataset("opus100", "en-ro", split = "train")

    ro_texts = []
    for i in range(2000):
        ro_texts.append(opus_ro[i]['translation']['ro'])

    df_ro = pd.DataFrame({'text': ro_texts, 'labels': 'ro'})

    dataset_final = pd.concat([
        df_papluca_final,
        df_ro
    ], ignore_index = True)

    return dataset_final

def prepare_main_dataset():
    wili = get_wili()
    tatoeba = get_tatoeba()

    TOTAL_PER_LANG = 2000
    wili_cnt = int(TOTAL_PER_LANG *0.70)
    tatoeba_cnt = int(TOTAL_PER_LANG *0.30)

    bucket = []

    for lang in TARGET_LAN:
        wili_lang = wili[wili['labels'] == lang]
        new_wili = min(len(wili_lang), wili_cnt)
        bucket.append(wili_lang.sample(n = new_wili, random_state = 42))

        tatoeba_lang = tatoeba[tatoeba['labels'] == lang]
        new_tatoeba = min(len(tatoeba_lang), tatoeba_cnt)
        bucket.append(tatoeba_lang.sample(n = new_tatoeba, random_state = 42))

    final_df = pd.concat(bucket, ignore_index = True)
    final_df = final_df.dropna(subset=['text'])
    final_df = final_df[final_df['text'].astype(str).str.strip()!= ""]
    final_df['text'] = final_df['text'].apply(clean_data)
    final_df = final_df[['labels', 'text']]


    train_data, temp_data = train_test_split(
        final_df,
        test_size = 0.30,
        stratify = final_df['labels'],
        random_state = 12
    )

    dev_data, test_data = train_test_split(
        temp_data,
        test_size = 0.50,
        stratify = temp_data['labels'],
        random_state = 12
    )

    train_data.to_csv("train.csv", index = False)
    dev_data.to_csv("dev.csv", index = False)
    test_data.to_csv("test.csv", index = False)

    print(f" In train.csv {len(train_data)} rows")
    print(f" In dev.csv {len(dev_data)} rows")
    print(f" In test.csv {len(test_data)} rows")


def main():
    prepare_main_dataset()

if __name__ == "__main__":
    main()