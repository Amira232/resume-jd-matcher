import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@st.cache_resource(show_spinner=False)
def load_sentence_model():
    # Load the pretrained Sentence Transformer only once and reuse it.
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("all-MiniLM-L6-v2")


def calculate_bow_similarity(resume_text, jd_text):
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    try:
        # Bag of Words represents documents using word/ngram frequency.
        vectorizer = CountVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        matrix = vectorizer.fit_transform(
            [resume_text, jd_text]
        )

        # Cosine similarity measures how similar the two vectors are.
        score = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        return float(score * 100)

    except ValueError:
        return 0.0


def calculate_tfidf_similarity(resume_text, jd_text):
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    try:
        # TF-IDF gives higher importance to informative words.
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        matrix = vectorizer.fit_transform(
            [resume_text, jd_text]
        )

        # Compare the TF-IDF vectors using cosine similarity.
        score = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        return float(score * 100)

    except ValueError:
        return 0.0


def calculate_semantic_similarity(resume_text, jd_text):
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    # Sentence Transformer converts text into semantic embeddings.
    model = load_sentence_model()

    embeddings = model.encode(
        [resume_text, jd_text],
        normalize_embeddings=True,
        show_progress_bar=False
    )

    # Dot product of normalized embeddings gives cosine similarity.
    score = float(embeddings[0] @ embeddings[1])
    score = max(0.0, min(1.0, score))

    return score * 100
