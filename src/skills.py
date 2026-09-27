import json
import re
from pathlib import Path


# Load the configured skill database from JSON.
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


def normalize_text(text):
    # Normalize text so skill matching is more consistent.
    if not text:
        return ""

    text = text.lower()

    # Normalize different dash characters.
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Normalize common separators.
    text = text.replace("•", " ")
    text = text.replace("|", " ")

    # Replace multiple spaces with a single space.
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def build_pattern(term):
    # Escape special regex characters before searching for a skill.
    term = normalize_text(term)
    escaped = re.escape(term)

    # Boundaries prevent partial matches inside unrelated words.
    return (
        r"(?<![a-z0-9+#])"
        + escaped
        + r"(?![a-z0-9+#])"
    )


def extract_skills(text):
    # Detect canonical skills using the configured skill database.
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


def get_skill_list(text):
    # Return detected skills in alphabetical order.
    skills = extract_skills(text)

    return sorted(
        skills.keys(),
        key=str.lower
    )


def get_skills_by_category(text):
    # Group detected skills according to their categories.
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


# Related skills help identify technologies that are connected
# even when the exact JD skill is not directly present.
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
    "Natural Language Processing": {"Machine Learning", "Deep Learning"},
    "Computer Vision": {"Deep Learning"},
    "Generative AI": {"Large Language Models", "Transformers"},
    "Large Language Models": {"Generative AI", "Transformers"},
    "Transformers": {"Large Language Models", "Generative AI"},

    "GitHub": {"Git"},
    "Kubernetes": {"Docker"},
    "Docker": {"Kubernetes"},
    "CI/CD": {"GitHub", "Git"},
}


def compare_skills(resume_skills, jd_skills):
    # Convert lists to sets for efficient skill comparison.
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    # Exact skill matches are the intersection of both sets.
    matched = sorted(
        resume_set.intersection(jd_set),
        key=str.lower
    )

    # Skills required by the JD but not directly found in the resume.
    missing_candidates = sorted(
        jd_set - resume_set,
        key=str.lower
    )

    related = []
    missing = []

    for jd_skill in missing_candidates:
        related_resume_skill = None

        possible_related = RELATED_SKILLS.get(
            jd_skill,
            set()
        )

        # Check whether a related technology exists in the resume.
        for possible_skill in sorted(
            possible_related,
            key=str.lower
        ):
            if possible_skill in resume_set:
                related_resume_skill = possible_skill
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

    return (
        matched,
        related,
        missing
    )


def get_skill_category(skill):
    # Find the category assigned to a canonical skill.
    for category, skills in SKILL_DATA.items():
        if skill in skills:
            return category

    return None


def get_all_skills():
    # Return every canonical skill from the skill database.
    skills = []

    for category, category_skills in SKILL_DATA.items():
        skills.extend(
            category_skills.keys()
        )

    return sorted(
        skills,
        key=str.lower
    )
