from src.skills import get_skill_list, compare_skills
from src.similarity import calculate_bow_similarity, calculate_tfidf_similarity, calculate_semantic_similarity
from src.ats import analyze_ats


def analyze(resume_text, jd_text):
    # Extract skills from the resume and job description.
    resume_skills = get_skill_list(resume_text)
    jd_skills = get_skill_list(jd_text)

    # Compare skills to find exact matches, related skills and missing skills.
    matched, related, missing = compare_skills(
        resume_skills,
        jd_skills
    )

    # Skill coverage = percentage of JD skills found directly in the resume.
    coverage = len(matched) / len(jd_skills) * 100 if jd_skills else 0
    coverage = round(coverage, 1)

    # Calculate similarity using different NLP/vectorization techniques.
    bow_score = calculate_bow_similarity(
        resume_text,
        jd_text
    )

    tfidf_score = calculate_tfidf_similarity(
        resume_text,
        jd_text
    )

    semantic_score = calculate_semantic_similarity(
        resume_text,
        jd_text
    )

    # Overall score combines skill coverage, semantic similarity and TF-IDF.
    alignment = (
        coverage * 0.50
        + semantic_score * 0.35
        + tfidf_score * 0.15
    )

    # Keep the final score between 0 and 100.
    alignment = round(
        max(0, min(100, alignment)),
        1
    )

    # Perform ATS checks for resume structure, keywords, contact and length.
    ats = analyze_ats(
        resume_text,
        jd_skills
    )

    suggestions = []

    if missing:
        suggestions.append(
            "Review missing skills and add them only if "
            "you genuinely have experience with them."
        )

    if related:
        suggestions.append(
            "Where accurate, make related technologies "
            "explicit in relevant projects or experience."
        )

    keyword_data = ats.get("keyword_analysis", {})

    if keyword_data.get("missing"):
        suggestions.append(
            "Add relevant missing JD keywords naturally "
            "to Skills, Projects or Experience when accurate."
        )

    important_sections = [
        "Skills",
        "Education",
        "Experience",
        "Projects"
    ]

    sections = ats.get("sections", {})

    missing_sections = [
        section
        for section in important_sections
        if not sections.get(section, False)
    ]

    if missing_sections:
        suggestions.append(
            "Consider adding clear resume sections for: "
            + ", ".join(missing_sections)
            + "."
        )

    contact = ats.get("contact", {})

    contact_fields = {
        "email": "Email",
        "phone": "Phone",
        "linkedin": "LinkedIn",
        "github": "GitHub"
    }

    missing_contact = [
        label
        for key, label in contact_fields.items()
        if not contact.get(key, False)
    ]

    if missing_contact:
        suggestions.append(
            "Consider adding missing contact/profile details: "
            + ", ".join(missing_contact)
            + "."
        )

    length = ats.get("length", {})

    if length.get("status") != "Good":
        suggestions.append(
            "Review resume length and keep content focused "
            "on information relevant to the target role."
        )

    return {
        "alignment": alignment,
        "coverage": coverage,
        "bow_score": round(bow_score, 1),
        "tfidf_score": round(tfidf_score, 1),
        "semantic_score": round(semantic_score, 1),
        "matched": matched,
        "related": related,
        "missing": missing,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "ats": ats,
        "suggestions": suggestions
    }
