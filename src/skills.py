import json
import re
from pathlib import Path


# ============================================================
# LOAD SKILL DATABASE
# ============================================================

SKILL_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "skills.json"
)

with open(
    SKILL_FILE,
    "r",
    encoding="utf-8"
) as file:
    SKILL_DATA = json.load(file)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize text before skill matching.
    """

    if not text:
        return ""

    text = text.lower()

    # Normalize different dash characters
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Normalize common separators
    text = text.replace("•", " ")
    text = text.replace("|", " ")

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# SAFE TERM PATTERN
# ============================================================

def build_pattern(term):
    """
    Build a regex pattern that avoids matching
    skills inside unrelated words.
    """

    term = normalize_text(term)

    escaped = re.escape(term)

    return (
        r"(?<![a-z0-9+#])"
        + escaped
        + r"(?![a-z0-9+#])"
    )


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text):
    """
    Detect canonical skills from the configured
    skill database.

    Returns:
        {
            "Python": "Programming",
            "FastAPI": "Backend",
            ...
        }
    """

    normalized = normalize_text(text)

    found = {}

    if not normalized:
        return found

    for category, skills in SKILL_DATA.items():

        for canonical_name, aliases in skills.items():

            possible_terms = [
                canonical_name
            ] + aliases

            for term in possible_terms:

                if not term:
                    continue

                pattern = build_pattern(term)

                if re.search(
                    pattern,
                    normalized
                ):

                    found[canonical_name] = category
                    break

    return found


# ============================================================
# SKILL LIST
# ============================================================

def get_skill_list(text):
    """
    Return a sorted list of detected canonical skills.
    """

    skills = extract_skills(text)

    return sorted(
        skills.keys(),
        key=str.lower
    )


# ============================================================
# SKILLS BY CATEGORY
# ============================================================

def get_skills_by_category(text):
    """
    Return detected skills grouped by category.

    Example:
        {
            "Programming": ["Python", "Java"],
            "Database": ["PostgreSQL"],
            "AI & Machine Learning": ["Machine Learning"]
        }
    """

    detected = extract_skills(text)

    grouped = {}

    for skill, category in detected.items():

        grouped.setdefault(
            category,
            []
        ).append(skill)

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


# ============================================================
# RELATED SKILLS
# ============================================================

RELATED_SKILLS = {

    # --------------------------------------------------------
    # Programming
    # --------------------------------------------------------

    "JavaScript": {
        "TypeScript"
    },

    "TypeScript": {
        "JavaScript"
    },

    # --------------------------------------------------------
    # Web
    # --------------------------------------------------------

    "React": {
        "JavaScript",
        "TypeScript"
    },

    "Angular": {
        "JavaScript",
        "TypeScript"
    },

    "Vue": {
        "JavaScript",
        "TypeScript"
    },

    "Node.js": {
        "JavaScript"
    },

    "Express.js": {
        "Node.js",
        "JavaScript"
    },

    # --------------------------------------------------------
    # Backend
    # --------------------------------------------------------

    "FastAPI": {
        "Python",
        "REST API"
    },

    "Flask": {
        "Python",
        "REST API"
    },

    "Django": {
        "Python",
        "REST API"
    },

    "REST API": {
        "FastAPI",
        "Flask",
        "Django"
    },

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    "PostgreSQL": {
        "MySQL",
        "SQLite"
    },

    "MySQL": {
        "PostgreSQL",
        "SQLite"
    },

    "MongoDB": {
        "Redis"
    },

    "Redis": {
        "MongoDB"
    },

    # --------------------------------------------------------
    # AI / ML
    # --------------------------------------------------------

    "Machine Learning": {
        "Scikit-learn",
        "Python"
    },

    "Scikit-learn": {
        "Machine Learning",
        "Python"
    },

    "Deep Learning": {
        "TensorFlow",
        "PyTorch"
    },

    "TensorFlow": {
        "Deep Learning",
        "Python"
    },

    "PyTorch": {
        "Deep Learning",
        "Python"
    },

    "Natural Language Processing": {
        "Machine Learning",
        "Deep Learning"
    },

    "Computer Vision": {
        "Deep Learning"
    },

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

    # --------------------------------------------------------
    # Cloud / DevOps
    # --------------------------------------------------------

    "GitHub": {
        "Git"
    },

    "Kubernetes": {
        "Docker"
    },

    "Docker": {
        "Kubernetes"
    },

    "CI/CD": {
        "GitHub",
        "Git"
    },
}


# ============================================================
# COMPARE SKILLS
# ============================================================

def compare_skills(
    resume_skills,
    jd_skills
):
    """
    Compare resume skills against JD skills.

    Returns:
        matched
        related
        missing

    related format:
        [
            ("Python", "FastAPI")
        ]
    """

    resume_set = set(
        resume_skills
    )

    jd_set = set(
        jd_skills
    )

    # --------------------------------------------------------
    # Exact matches
    # --------------------------------------------------------

    matched = sorted(
        resume_set.intersection(jd_set),
        key=str.lower
    )

    # --------------------------------------------------------
    # Skills not directly matched
    # --------------------------------------------------------

    missing_candidates = sorted(
        jd_set - resume_set,
        key=str.lower
    )

    related = []
    missing = []

    # --------------------------------------------------------
    # Related skill matching
    # --------------------------------------------------------

    for jd_skill in missing_candidates:

        related_resume_skill = None

        possible_related = RELATED_SKILLS.get(
            jd_skill,
            set()
        )

        # Prefer a directly detected related skill
        for possible_skill in sorted(
            possible_related,
            key=str.lower
        ):

            if possible_skill in resume_set:

                related_resume_skill = (
                    possible_skill
                )

                break

        if related_resume_skill:

            related.append(
                (
                    related_resume_skill,
                    jd_skill
                )
            )

        else:

            missing.append(
                jd_skill
            )

    return (
        matched,
        related,
        missing
    )


# ============================================================
# SKILL CATEGORY LOOKUP
# ============================================================

def get_skill_category(skill):
    """
    Return the category of a canonical skill.
    """

    for category, skills in SKILL_DATA.items():

        if skill in skills:
            return category

    return None


# ============================================================
# SKILL DATABASE ACCESS
# ============================================================

def get_all_skills():
    """
    Return all canonical skills.
    """

    skills = []

    for category, category_skills in SKILL_DATA.items():

        skills.extend(
            category_skills.keys()
        )

    return sorted(
        skills,
        key=str.lower
    )