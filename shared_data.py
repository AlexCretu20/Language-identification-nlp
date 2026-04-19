import re
TARGET_LAN = [
    'en',
    'ro',
    'fr',
    'es',
    'de',
    'it',
    'pt',
    'nl',
    'pl',
    'tr',
    'ar',
    'zh',
    'ja'
]

LANG_MAP = {
    'eng': 'en',
    'ron': 'ro',
    'fra': 'fr',
    'spa': 'es',
    'deu': 'de',
    'ita': 'it',
    'por': 'pt',
    'nld': 'nl',
    'pol': 'pl',
    'tur': 'tr',
    'ara': 'ar',
    'zho': 'zh',
    'jpn': 'ja'

}

def clean_data(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()