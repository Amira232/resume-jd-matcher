import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@st.cache_resource(show_spinner=False)
def load_sentence_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


def calculate_bow_similarity(resume_text, jd_text):
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    try:
        vectorizer = CountVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        matrix = vectorizer.fit_transform(
            [resume_text, jd_text]
        )

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
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        matrix = vectorizer.fit_transform(
            [resume_text, jd_text]
        )

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

    model = load_sentence_model()

    embeddings = model.encode(
        [resume_text, jd_text],
        normalize_embeddings=True,
        show_progress_bar=False
    )

    score = float(embeddings[0] @ embeddings[1])
    score = max(0.0, min(1.0, score))

    return score * 100