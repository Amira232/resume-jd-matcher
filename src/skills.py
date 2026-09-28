import json
import re
from pathlib import Path


SKILL_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "skills.json"
)

with open(SKILL_FILE, "r", encoding="utf-8") as file:
    SKILL_DATA = json.load(file)


EXCLUDED_SKILLS = {
    "teamwork"
}


def normalize_text(text):
    if not text:
        return ""

    text = text.lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("•", " ")
    text = text.replace("|", " ")

    # Treat REST API variations as the same term.
    text = re.sub(r"\brestful\s+apis?\b", "rest api", text)
    text = re.sub(r"\brest\s+apis?\b", "rest api", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_skill(skill):
    return normalize_text(skill)


def build_pattern(term):
    term = normalize_text(term)

    return (
        r"(?<![a-z0-9+#])"
        + re.escape(term)
        + r"(?![a-z0-9+#])"
    )


def is_excluded(skill):
    return normalize_skill(skill) in EXCLUDED_SKILLS


def extract_skills(text):
    normalized = normalize_text(text)

    if not normalized:
        return {}

    found = {}

    for category, skills in SKILL_DATA.items():
        for canonical_name, aliases in skills.items():

            if is_excluded(canonical_name):
                continue

            possible_terms = [canonical_name] + aliases

            for term in possible_terms:
                if not term or is_excluded(term):
                    continue

                if re.search(
                    build_pattern(term),
                    normalized
                ):
                    found[canonical_name] = category
                    break

    return found


def get_skill_list(text):
    return sorted(
        extract_skills(text).keys(),
        key=str.lower
    )


def get_skills_by_category(text):
    detected = extract_skills(text)
    grouped = {}

    for skill, category in detected.items():
        grouped.setdefault(category, []).append(skill)

    for category in grouped:
        grouped[category] = sorted(
            grouped[category],
            key=str.lower
        )

    return dict(
        sorted(
            grouped.items(),
            key=lambda item: item[0].lower()
        )
    )


RELATED_SKILLS = {
    "JavaScript": {"TypeScript"},
    "TypeScript": {"JavaScript"},

    "React": {"JavaScript", "TypeScript"},
    "Angular": {"JavaScript", "TypeScript"},
    "Vue": {"JavaScript", "TypeScript"},
    "Node.js": {"JavaScript"},
    "Express.js": {"Node.js", "JavaScript"},

    "FastAPI": {"Python", "REST API"},
    "Flask": {"Python", "REST API"},
    "Django": {"Python", "REST API"},
    "REST API": {"FastAPI", "Flask", "Django"},

    "PostgreSQL": {"MySQL", "SQLite"},
    "MySQL": {"PostgreSQL", "SQLite"},

    "MongoDB": {"Redis"},
    "Redis": {"MongoDB"},

    "Machine Learning": {"Scikit-learn", "Python"},
    "Scikit-learn": {"Machine Learning", "Python"},

    "Deep Learning": {"TensorFlow", "PyTorch"},
    "TensorFlow": {"Deep Learning", "Python"},
    "PyTorch": {"Deep Learning", "Python"},

    "Natural Language Processing": {
        "Machine Learning",
        "Deep Learning"
    },

    "Computer Vision": {"Deep Learning"},

    "Generative AI": {
        "Large Language Models",
        "Transformers"
    },

    "Large Language Models": {
        "Generative AI",
        "Transformers"
    },

    "Transformers": {
        "Large Language Models",
        "Generative AI"
    },

    "GitHub": {"Git"},
    "Kubernetes": {"Docker"},
    "Docker": {"Kubernetes"},
    "CI/CD": {"GitHub", "Git"}
}


def compare_skills(resume_skills, jd_skills):
    resume_map = {
        normalize_skill(skill): skill
        for skill in resume_skills
        if not is_excluded(skill)
    }

    jd_map = {
        normalize_skill(skill): skill
        for skill in jd_skills
        if not is_excluded(skill)
    }

    matched_keys = set(resume_map) & set(jd_map)

    matched = sorted(
        [jd_map[key] for key in matched_keys],
        key=str.lower
    )

    missing_candidates = sorted(
        set(jd_map) - set(resume_map),
        key=str.lower
    )

    related_map = {
        normalize_skill(key): {
            normalize_skill(value)
            for value in values
        }
        for key, values in RELATED_SKILLS.items()
    }

    related = []
    missing = []

    for jd_skill in missing_candidates:
        jd_key = normalize_skill(jd_skill)
        possible_related = related_map.get(
            jd_key,
            set()
        )

        related_resume_skill = None

        for resume_key, resume_skill in resume_map.items():
            if resume_key in possible_related:
                related_resume_skill = resume_skill
                break

        if related_resume_skill:
            related.append(
                (
                    related_resume_skill,
                    jd_skill
                )
            )
        else:
            missing.append(jd_skill)

    return matched, related, missing


def get_skill_category(skill):
    for category, skills in SKILL_DATA.items():
        for canonical_name in skills:
            if normalize_skill(canonical_name) == normalize_skill(skill):
                return category

    return None


def get_all_skills():
    skills = []

    for category_skills in SKILL_DATA.values():
        for skill in category_skills:
            if not is_excluded(skill):
                skills.append(skill)

    return sorted(
        skills,
        key=str.lower
    )
