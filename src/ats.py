import re


# Regex patterns used to detect common resume sections.
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
    # Lowercase text makes regex matching case-insensitive.
    text = text.lower()

    # Regex is used to detect common contact information patterns.
    email = bool(
        re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            text
        )
    )

    phone = bool(
        re.search(
            r"(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}",
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
    text = text.lower()

    # Check whether at least one regex pattern exists for each section.
    return {
        section: any(
            re.search(pattern, text)
            for pattern in patterns
        )
        for section, patterns in SECTION_PATTERNS.items()
    }


def analyze_length(text):
    # Count words using a regex pattern.
    word_count = len(re.findall(r"\b\w+\b", text))

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
    if not jd_skills:
        return 0

    resume_text = resume_text.lower()

    # Count JD skills that appear directly in the resume.
    matched = sum(
        bool(
            re.search(
                rf"(?<![a-z0-9+#]){re.escape(skill.lower())}"
                r"(?![a-z0-9+#])",
                resume_text
            )
        )
        for skill in jd_skills
    )

    return round(matched / len(jd_skills) * 100)


def keyword_analysis(resume_text, jd_skills):
    resume_text = resume_text.lower()
    matched = []
    missing = []

    # Separate JD keywords into matched and missing groups.
    for skill in jd_skills:
        pattern = (
            rf"(?<![a-z0-9+#]){re.escape(skill.lower())}"
            r"(?![a-z0-9+#])"
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

    # Calculate the percentage of important resume sections detected.
    section_score = (
        sum(sections.get(x, False) for x in important_sections)
        / len(important_sections)
        * 100
    )

    # Calculate the percentage of contact details detected.
    contact_score = (
        sum(contact.values()) / len(contact) * 100
        if contact else 0
    )

    # Convert resume length status into a numeric score.
    length_score = {
        "Good": 100,
        "Long": 80,
        "Too short": 65,
        "Very long": 55
    }.get(length["status"], 0)

    # Weighted ATS score.
    score = (
        keyword_score * 0.50
        + section_score * 0.25
        + contact_score * 0.15
        + length_score * 0.10
    )

    return round(max(0, min(100, score)))


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
