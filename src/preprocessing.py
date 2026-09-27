import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def download_nltk_resources():
    # Download NLP resources only when they are not already available.
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
    # Tokenization splits text into individual words/tokens.
    if not text:
        return []

    return word_tokenize(text)


def preprocess_text(text):
    if not text:
        return []

    # Lowercasing makes words such as "Python" and "python" equivalent.
    text = text.lower()

    # Tokenization converts the text into individual tokens.
    tokens = tokenize_text(text)
    cleaned_tokens = []

    for token in tokens:
        # Remove punctuation tokens.
        if token in string.punctuation:
            continue

        # Ignore tokens that contain no letters or numbers.
        if not re.search(r"[a-z0-9]", token):
            continue

        # Remove common English stop words such as "the", "is", and "and".
        if token in STOP_WORDS:
            continue

        # Lemmatization converts words to their base dictionary form.
        lemma = LEMMATIZER.lemmatize(token)
        cleaned_tokens.append(lemma)

    return cleaned_tokens


def get_preprocessed_text(text):
    # Convert the processed token list back into a text string.
    return " ".join(preprocess_text(text))


def get_preprocessing_info(text):
    if not text:
        return {
            "original_tokens": [],
            "processed_tokens": [],
            "original_count": 0,
            "processed_count": 0
        }

    # Used when displaying or checking preprocessing statistics.
    original_tokens = tokenize_text(text.lower())
    processed_tokens = preprocess_text(text)

    return {
        "original_tokens": original_tokens,
        "processed_tokens": processed_tokens,
        "original_count": len(original_tokens),
        "processed_count": len(processed_tokens)
    }
