import re

from src.skills import normalize_text, normalize_skill


SECTION_PATTERNS = {
    "Contact": [
        r"\bcontact\b",
        r"\bemail\b",
        r"\bphone\b",
        r"\blinkedin\b",
        r"\bgithub\b"
    ],
    "Summary / Objective": [
        r"\bsummary\b",
        r"\bprofessional summary\b",
        r"\bobjective\b",
        r"\bcareer objective\b",
        r"\bprofile\b"
    ],
    "Skills": [
        r"\bskills\b",
        r"\btechnical skills\b",
        r"\bcore skills\b",
        r"\bskills\s*&\s*technologies\b"
    ],
    "Education": [
        r"\beducation\b",
        r"\bacademic background\b",
        r"\bqualifications\b"
    ],
    "Experience": [
        r"\bexperience\b",
        r"\bwork experience\b",
        r"\bprofessional experience\b",
        r"\binternship\b",
        r"\binternships\b"
    ],
    "Projects": [
        r"\bprojects\b",
        r"\bpersonal projects\b",
        r"\bacademic projects\b",
        r"\bproject experience\b"
    ],
    "Certifications": [
        r"\bcertifications\b",
        r"\bcertificates\b",
        r"\blicenses\b"
    ]
}


def check_contact_information(text):
    text = normalize_text(text)

    email = bool(
        re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            text
        )
    )

    phone = bool(
        re.search(
            r"(?<!\d)(?:\+91[\s.-]*)?(?:[6-9]\d{4}[\s.-]*\d{5})(?!\d)",
            text
        )
    )

    linkedin = bool(
        re.search(
            r"\b(?:https?://)?(?:www\.)?linkedin\.com/",
            text
        )
    )

    github = bool(
        re.search(
            r"\b(?:https?://)?(?:www\.)?github\.com/",
            text
        )
    )

    return {
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github
    }


def detect_sections(text):
    text = normalize_text(text)

    return {
        section: any(
            re.search(pattern, text)
            for pattern in patterns
        )
        for section, patterns in SECTION_PATTERNS.items()
    }


def analyze_length(text):
    word_count = len(
        re.findall(
            r"\b\w+\b",
            text
        )
    )

    if word_count < 150:
        status = "Too short"
    elif word_count <= 900:
        status = "Good"
    elif word_count <= 1200:
        status = "Long"
    else:
        status = "Very long"

    return {
        "word_count": word_count,
        "status": status
    }


def keyword_coverage(resume_text, jd_skills):
    resume_text = normalize_text(resume_text)

    if not jd_skills:
        return 0

    matched = 0

    for skill in jd_skills:
        pattern = (
            r"(?<![a-z0-9+#])"
            + re.escape(normalize_skill(skill))
            + r"(?![a-z0-9+#])"
        )

        if re.search(pattern, resume_text):
            matched += 1

    return round(
        matched / len(jd_skills) * 100
    )


def keyword_analysis(resume_text, jd_skills):
    resume_text = normalize_text(resume_text)

    matched = []
    missing = []

    for skill in jd_skills:
        pattern = (
            r"(?<![a-z0-9+#])"
            + re.escape(normalize_skill(skill))
            + r"(?![a-z0-9+#])"
        )

        if re.search(pattern, resume_text):
            matched.append(skill)
        else:
            missing.append(skill)

    return {
        "matched": matched,
        "missing": missing,
        "match_count": len(matched),
        "missing_count": len(missing)
    }


def calculate_ats_score(
    sections,
    contact,
    length,
    keyword_score
):
    important_sections = [
        "Skills",
        "Education",
        "Experience",
        "Projects"
    ]

    section_score = (
        sum(
            sections.get(x, False)
            for x in important_sections
        )
        / len(important_sections)
        * 100
    )

    contact_score = (
        sum(contact.values())
        / len(contact)
        * 100
        if contact
        else 0
    )

    length_score = {
        "Good": 100,
        "Long": 80,
        "Too short": 65,
        "Very long": 55
    }.get(
        length["status"],
        0
    )

    score = (
        keyword_score * 0.50
        + section_score * 0.25
        + contact_score * 0.15
        + length_score * 0.10
    )

    return round(
        max(0, min(100, score))
    )


def analyze_ats(resume_text, jd_skills):
    sections = detect_sections(resume_text)
    contact = check_contact_information(resume_text)
    length = analyze_length(resume_text)

    keyword_score = keyword_coverage(
        resume_text,
        jd_skills
    )

    keyword_data = keyword_analysis(
        resume_text,
        jd_skills
    )

    score = calculate_ats_score(
        sections,
        contact,
        length,
        keyword_score
    )

    return {
        "score": score,
        "sections": sections,
        "contact": contact,
        "length": length,
        "keyword_score": keyword_score,
        "keyword_analysis": keyword_data
    }
