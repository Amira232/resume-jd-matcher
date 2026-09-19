import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def download_nltk_resources():
    resources = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4")
    ]

    for path, resource in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(resource, quiet=True)


download_nltk_resources()

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()


def tokenize_text(text):
    if not text:
        return []
    return word_tokenize(text)


def preprocess_text(text):
    if not text:
        return []

    text = text.lower()
    tokens = tokenize_text(text)
    cleaned_tokens = []

    for token in tokens:
        if token in string.punctuation:
            continue

        if not re.search(r"[a-z0-9]", token):
            continue

        if token in STOP_WORDS:
            continue

        lemma = LEMMATIZER.lemmatize(token)
        cleaned_tokens.append(lemma)

    return cleaned_tokens


def get_preprocessed_text(text):
    return " ".join(preprocess_text(text))


def get_preprocessing_info(text):
    if not text:
        return {
            "original_tokens": [],
            "processed_tokens": [],
            "original_count": 0,
            "processed_count": 0
        }

    original_tokens = tokenize_text(text.lower())
    processed_tokens = preprocess_text(text)

    return {
        "original_tokens": original_tokens,
        "processed_tokens": processed_tokens,
        "original_count": len(original_tokens),
        "processed_count": len(processed_tokens)
    }