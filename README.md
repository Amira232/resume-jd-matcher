# ResumeMatch — NLP-Based Resume–Job Description Matcher

## 📌 Problem Statement

Recruiters and applicants need to compare resumes with job descriptions to identify relevant skills and requirements. Manual comparison can be time-consuming and may overlook important keywords or semantic similarities.

**ResumeMatch** uses Natural Language Processing to automatically analyze a resume against a job description, identify matching and missing skills, calculate lexical and semantic similarity, and provide ATS-oriented resume insights.

---

## 🚀 Live Demo

**[Try ResumeMatch](https://resume-jd-matcher-dpr2lnum9nlnftkjt7xism.streamlit.app/)**

---

## 🔄 Pipeline Architecture

```text
Resume + Job Description
          │
          ▼
     Text Extraction
          │
          ▼
   NLP Preprocessing
          │
   ┌──────┼─────────┐
   │      │         │
   ▼      ▼         ▼
Tokenize  Stop    Lemmatize
Lowercase Words
Punctuation Removal
   │      │         │
   └──────┼─────────┘
          ▼
    Processed Text
          │
    ┌─────┼──────────────┐
    │     │              │
    ▼     ▼              ▼
   BoW  TF-IDF        N-grams
    │     │        Uni/Bi/Tri
    └─────┼──────────────┘
          ▼
    Lexical Similarity
          │
          ▼
   Semantic Similarity
          │
          ▼
    Skill Extraction
          │
          ▼
     Skill Matching
          │
          ▼
      ATS Analysis
          │
          ▼
   Final Analysis Report
```

---

## Features

| Feature              | Description                                                                         |
| -------------------- | ----------------------------------------------------------------------------------- |
| Resume Upload        | Supports PDF, DOCX and TXT files                                                    |
| Text Preprocessing   | Tokenization, lowercasing, punctuation removal, stop-word removal and lemmatization |
| Bag of Words         | Calculates lexical similarity using word-frequency vectors                          |
| TF-IDF               | Calculates similarity using TF-IDF representations                                  |
| N-gram Analysis      | Generates unigrams, bigrams and trigrams                                            |
| Semantic Similarity  | Uses Sentence Transformer embeddings to compare meaning                             |
| Skill Extraction     | Detects skills from resumes and job descriptions                                    |
| Skill Matching       | Identifies direct, related and missing skills                                       |
| Overall Resume Match | Combines skill coverage and similarity measures                                     |
| ATS Analysis         | Checks keywords, resume sections, contact information and length                    |
| Recommendations      | Provides suggestions based on detected gaps                                         |

---

## NLP Techniques

| NLP Technique       | Application in ResumeMatch                          |
| ------------------- | --------------------------------------------------- |
| Tokenization        | Converts text into individual tokens                |
| Lowercasing         | Normalizes text to lowercase                        |
| Punctuation Removal | Removes unnecessary punctuation                     |
| Stop-word Removal   | Removes common English words                        |
| Lemmatization       | Converts words to their base form                   |
| Bag of Words        | Represents text using word frequencies              |
| TF-IDF              | Represents the importance of words in documents     |
| N-grams             | Generates unigram, bigram and trigram sequences     |
| Cosine Similarity   | Measures similarity between text vectors            |
| Sentence Embeddings | Captures semantic meaning using a pre-trained model |

---

## Tech Stack

| Category            | Library / Technology  |
| ------------------- | --------------------- |
| Language            | Python                |
| User Interface      | Streamlit             |
| NLP Preprocessing   | NLTK                  |
| Text Vectorization  | Scikit-learn          |
| Similarity          | Scikit-learn          |
| Semantic Embeddings | Sentence Transformers |
| PDF Processing      | PyPDF                 |
| DOCX Processing     | python-docx           |
| Skill Database      | JSON                  |

---

## 📁 Repository Structure

```text
resume-jd-matcher/
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   └── skills.json
│
├── src/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── ats.py
│   ├── parser.py
│   ├── similarity.py
│   └── skills.py
│
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

---

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Amira232/resume-jd-matcher.git
cd resume-jd-matcher
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The application will open in your browser.
