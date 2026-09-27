import streamlit as st

from src.parser import extract_text
from src.analyzer import analyze


st.set_page_config(
    page_title="ResumeMatch",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #F8FAFC;
    --card: #FFFFFF;
    --text: #0F172A;
    --muted: #64748B;
    --subtle: #94A3B8;
    --border: #E2E8F0;
    --blue: #4F46E5;
    --blue-dark: #4338CA;
    --green: #059669;
    --green-bg: #ECFDF5;
    --rose: #E11D48;
    --rose-bg: #FFF1F2;
    --amber: #D97706;
    --amber-bg: #FFFBEB;
}

* {
    font-family: "Inter", sans-serif;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1280px;
    padding: 36px 28px 70px;
}

h1, h2, h3 {
    color: var(--text) !important;
}

p {
    color: var(--muted);
}

[data-testid="stHorizontalBlock"],
[data-testid="column"],
[data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.hero {
    padding: 4px 0 30px;
}

.brand {
    color: var(--blue);
    font-size: 21px;
    font-weight: 800;
    letter-spacing: 1.4px;
    margin-bottom: 14px;
}

.hero-title {
    color: var(--text);
    font-size: 34px;
    line-height: 1.2;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 10px;
}

.hero-description {
    max-width: 760px;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.65;
}

.section-header {
    margin: 38px 0 18px;
}

.section-title {
    color: var(--text);
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.3px;
}

.section-description {
    color: var(--muted);
    font-size: 12px;
    margin-top: 4px;
}

.step-label {
    color: var(--blue);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 7px;
}

.card-title {
    color: var(--text);
    font-size: 17px;
    font-weight: 750;
    margin-bottom: 5px;
}

.card-description {
    color: var(--muted);
    font-size: 12px;
    line-height: 1.5;
    margin-bottom: 12px;
}

[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border: 1px dashed #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 5px !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: #FFFFFF !important;
    border: none !important;
    min-height: 145px !important;
    border-radius: 9px !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: var(--muted) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] div,
[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: var(--muted) !important;
}

[data-testid="stFileUploader"] button {
    background: #FFFFFF !important;
    color: var(--text) !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 7px !important;
    font-weight: 600 !important;
}

[data-testid="stFileUploader"] button:hover {
    color: var(--blue) !important;
    border-color: var(--blue) !important;
}

textarea {
    background: #FFFFFF !important;
    color: var(--text) !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    line-height: 1.55 !important;
    padding: 12px !important;
    box-shadow: none !important;
}

textarea:focus {
    border-color: #94A3B8 !important;
    box-shadow: 0 0 0 1px #CBD5E1 !important;
}

.stButton > button {
    background: var(--blue) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 9px !important;
    min-height: 48px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    box-shadow: 0 5px 14px rgba(79, 70, 229, 0.22) !important;
    transition: all 0.2s ease !important;
}

.stButton > button p,
.stButton > button span {
    color: #FFFFFF !important;
}

.stButton > button:hover {
    background: var(--blue-dark) !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0);
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 17px;
    min-height: 108px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
}

.metric-label {
    color: var(--muted);
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.metric-value {
    color: var(--text) !important;
    font-size: 28px;
    line-height: 1.2;
    font-weight: 800;
    margin-top: 7px;
}

.metric-note {
    color: var(--muted);
    font-size: 11px;
    margin-top: 4px;
}

.panel {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
}

.panel-title {
    color: var(--text);
    font-size: 14px;
    font-weight: 750;
    margin-bottom: 3px;
}

.panel-description {
    color: var(--muted);
    font-size: 11px;
    line-height: 1.5;
}

.stProgress {
    margin-top: 8px;
}

[data-testid="stProgressBar"] {
    background: #E2E8F0 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 999px !important;
    height: 9px !important;
    overflow: hidden !important;
}

[data-testid="stProgressBar"] > div {
    background: #E2E8F0 !important;
    border-radius: 999px !important;
}

[data-testid="stProgressBar"] > div > div {
    background: var(--blue) !important;
    border-radius: 999px !important;
}

.chip {
    display: inline-block;
    padding: 6px 10px;
    margin: 3px 4px 3px 0;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 600;
}

.chip-match {
    color: #047857;
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
}

.chip-missing {
    color: #BE123C;
    background: #FFF1F2;
    border: 1px solid #FECDD3;
}

.chip-related {
    color: #B45309;
    background: #FFFBEB;
    border: 1px solid #FDE68A;
}

.status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 0;
    border-bottom: 1px solid #F1F5F9;
}

.status-row:last-child {
    border-bottom: none;
}

.status-name {
    color: var(--text);
    font-size: 12px;
    font-weight: 600;
}

.status-pill {
    padding: 4px 9px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 700;
}

.status-present {
    color: #047857;
    background: var(--green-bg);
}

.status-missing {
    color: #BE123C;
    background: var(--rose-bg);
}

.alert-item {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-left: 3px solid var(--amber);
    border-radius: 9px;
    padding: 13px 14px;
    margin-bottom: 9px;
    color: #475569;
    font-size: 12px;
    line-height: 1.55;
}

.alert-title {
    color: var(--text);
    font-weight: 700;
    margin-bottom: 3px;
}

.file-ready {
    background: var(--green-bg);
    border: 1px solid #A7F3D0;
    color: #047857;
    border-radius: 8px;
    padding: 7px 10px;
    margin-top: 9px;
    font-size: 11px;
    font-weight: 600;
}

[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 14px !important;
}

[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: 11px !important;
}

[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-weight: 800 !important;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


def chips(items, css_class):
    if not items:
        return '<span class="chip" style="color:#64748B;background:#F1F5F9;border:1px solid #E2E8F0;">None detected</span>'

    return "".join(
        f'<span class="chip {css_class}">{item}</span>'
        for item in items
    )


def status_rows(items):
    html = ""

    for name, present in items:
        status_class = "status-present" if present else "status-missing"
        status_text = "Present" if present else "Missing"

        html += (
            f'<div class="status-row">'
            f'<span class="status-name">{name}</span>'
            f'<span class="status-pill {status_class}">{status_text}</span>'
            f'</div>'
        )

    return html


st.markdown(
    '<div class="hero">'
    '<div class="brand">ResumeMatch</div>'
    '<div class="hero-title">Measure your job fit before you apply.</div>'
    '<div class="hero-description">'
    'Analyze your resume against a target job description, identify relevant '
    'skills, uncover gaps and evaluate ATS readiness before you apply.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


resume_col, jd_col = st.columns(2, gap="large")

with resume_col:
    st.markdown(
        '<div class="step-label">01 · Resume</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">Upload your resume</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-description">'
        'Upload a PDF, DOCX or TXT resume for analysis.'
        '</div>',
        unsafe_allow_html=True
    )

    resume_file = st.file_uploader(
        "Resume",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed"
    )

    if resume_file:
        st.markdown(
            f'<div class="file-ready">✓ {resume_file.name} ready for analysis</div>',
            unsafe_allow_html=True
        )


with jd_col:
    st.markdown(
        '<div class="step-label">02 · Target role</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">Job description</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-description">'
        'Paste the complete job description to improve matching accuracy.'
        '</div>',
        unsafe_allow_html=True
    )

    jd_text = st.text_area(
        "Job description",
        height=165,
        placeholder="Paste the job description here...",
        label_visibility="collapsed"
    )


st.markdown(
    "<div style='height:18px'></div>",
    unsafe_allow_html=True
)

_, button_col, _ = st.columns([2.4, 1.4, 2.4])

with button_col:
    analyze_button = st.button(
        "Analyze Resume",
        type="primary",
        use_container_width=True
    )


if analyze_button:
    if resume_file is None:
        st.warning(
            "Please upload your resume.",
            icon="⚠️"
        )
        st.stop()

    if not jd_text.strip():
        st.warning(
            "Please paste the job description.",
            icon="⚠️"
        )
        st.stop()

    try:
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text(resume_file)
            result = analyze(
                resume_text,
                jd_text
            )

        st.session_state["analysis_result"] = result

        st.success(
            "Analysis completed successfully.",
            icon="✅"
        )

    except Exception as error:
        st.error(
            "Analysis failed. Please check the uploaded file and try again.",
            icon="❌"
        )

        with st.expander("Technical details"):
            st.exception(error)

        st.stop()


if "analysis_result" not in st.session_state:
    st.stop()


result = st.session_state["analysis_result"]
ats = result.get("ats", {})

alignment = float(
    result.get("alignment", 0)
)

coverage = float(
    result.get("coverage", 0)
)

bow_score = float(
    result.get("bow_score", 0)
)

tfidf_score = float(
    result.get("tfidf_score", 0)
)

ats_score = float(
    ats.get("score", 0)
)

matched = result.get(
    "matched",
    []
)

related = result.get(
    "related",
    []
)

missing = result.get(
    "missing",
    []
)

jd_skills = result.get(
    "jd_skills",
    [] 
)


st.markdown(
    '<div class="section-header">'
    '<div class="section-title">Application overview</div>'
    '<div class="section-description">'
    "A quick view of your resume's alignment with the target role."
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


overview_col, metrics_col = st.columns(
    [1.2, 2],
    gap="medium"
)


with overview_col:
    if alignment >= 80:
        description = "Strong alignment with the target role."
    elif alignment >= 60:
        description = "Good alignment with several areas to improve."
    elif alignment >= 40:
        description = "Moderate alignment with noticeable skill gaps."
    else:
        description = "Low alignment. Review the missing requirements."

    st.markdown(
        f'''
        <div class="panel">
            <div class="metric-label">Overall resume match</div>
            <div class="metric-value">{alignment:.1f}%</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.progress(
        max(0, min(alignment, 100)) / 100
    )

    st.markdown(
        f'''
        <div class="panel-description"
        style="margin-top:10px;">
        {description}
        </div>
        ''',
        unsafe_allow_html=True
    )


with metrics_col:
    m1, m2, m3 = st.columns(
        3,
        gap="medium"
    )

    with m1:
        st.markdown(
            f'''
            <div class="metric-card">
                <div class="metric-label">Skill coverage</div>
                <div class="metric-value">{coverage:.1f}%</div>
                <div class="metric-note">JD skills detected</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f'''
            <div class="metric-card">
                <div class="metric-label">ATS score</div>
                <div class="metric-value">{ats_score:.0f}%</div>
                <div class="metric-note">Resume readiness</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with m3:
        st.markdown(
            f'''
            <div class="metric-card">
                <div class="metric-label">JD skills</div>
                <div class="metric-value">{len(jd_skills)}</div>
                <div class="metric-note">Detected requirements</div>
            </div>
            ''',
            unsafe_allow_html=True
        )


st.markdown(
    '<div class="section-header">'
    '<div class="section-title">Lexical similarity</div>'
    '<div class="section-description">'
    'Compare resume and job description using traditional text vectorization techniques.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


lexical_col1, lexical_col2 = st.columns(
    2,
    gap="medium"
)


with lexical_col1:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-label">Bag of Words</div>
            <div class="metric-value">{bow_score:.1f}%</div>
            <div class="metric-note">Lexical similarity</div>
        </div>
        ''',
        unsafe_allow_html=True
    )


with lexical_col2:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-label">TF-IDF</div>
            <div class="metric-value">{tfidf_score:.1f}%</div>
            <div class="metric-note">Weighted lexical similarity</div>
        </div>
        ''',
        unsafe_allow_html=True
    )


st.markdown(
    '<div class="section-header">'
    '<div class="section-title">Skill analysis</div>'
    '<div class="section-description">'
    'Compare skills detected in your resume against the target job.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


c1, c2, c3 = st.columns(
    3,
    gap="medium"
)


with c1:
    st.metric(
        "Direct matches",
        len(matched)
    )


with c2:
    st.metric(
        "Related skills",
        len(related)
    )


with c3:
    st.metric(
        "Missing skills",
        len(missing)
    )


skill_left, skill_right = st.columns(
    2,
    gap="medium"
)


with skill_left:
    st.markdown(
        f'''
        <div class="panel">
            <div class="panel-title">Matched skills</div>
            <div class="panel-description">
                Skills directly detected in both documents.
            </div>
            <div style="margin-top:10px;">
                {chips(matched, "chip-match")}
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )


with skill_right:
    st.markdown(
        f'''
        <div class="panel">
            <div class="panel-title">Missing skills</div>
            <div class="panel-description">
                JD skills not directly detected in the resume.
            </div>
            <div style="margin-top:10px;">
                {chips(missing, "chip-missing")}
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )


if related:
    st.markdown(
        '<div style="height:14px"></div>',
        unsafe_allow_html=True
    )

    related_rows = "".join(
        [
            f'''
            <div class="status-row">
                <span class="status-name">{r_skill}</span>
                <span class="status-pill status-present">
                    Related to {j_skill}
                </span>
            </div>
            '''
            for r_skill, j_skill in related
        ]
    )

    st.markdown(
        f'''
        <div class="panel">
            <div class="panel-title">Related skills</div>
            <div class="panel-description">
                Related technologies detected in your resume.
            </div>
            {related_rows}
        </div>
        ''',
        unsafe_allow_html=True
    )


st.markdown(
    '<div class="section-header">'
    '<div class="section-title">ATS readiness</div>'
    '<div class="section-description">'
    'Resume structure, keywords, contact information and length.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


ats_score_col, ats_breakdown_col = st.columns(
    [1, 2],
    gap="medium"
)


with ats_score_col:
    st.markdown(
        f'''
        <div class="panel">
            <div class="panel-title">ATS score</div>
            <div class="panel-description">
                Overall ATS-oriented assessment.
            </div>
            <div class="metric-value">
                {ats_score:.0f}%
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.progress(
        max(0, min(ats_score, 100)) / 100
    )

    if ats_score >= 80:
        st.success(
            "Strong ATS readiness.",
            icon="✅"
        )
    elif ats_score >= 60:
        st.warning(
            "Some ATS improvements are recommended.",
            icon="⚠️"
        )
    else:
        st.error(
            "Several ATS improvements are recommended.",
            icon="❗"
        )


with ats_breakdown_col:
    sections = ats.get(
        "sections",
        {}
    )

    important_sections = [
        "Skills",
        "Education",
        "Experience",
        "Projects"
    ]

    section_values = [
        sections.get(
            section,
            False
        )
        for section in important_sections
    ]

    structure_score = (
        round(
            sum(section_values)
            / len(section_values)
            * 100
        )
        if section_values
        else 0
    )

    contact = ats.get(
        "contact",
        {}
    )

    contact_score = (
        round(
            sum(contact.values())
            / len(contact)
            * 100
        )
        if contact
        else 0
    )

    length = ats.get(
        "length",
        {}
    )

    length_status = length.get(
        "status",
        "Unknown"
    )

    length_scores = {
        "Good": 100,
        "Long": 80,
        "Too short": 65,
        "Very long": 55
    }

    length_score = length_scores.get(
        length_status,
        55
    )

    checks = [
        (
            "JD keyword coverage",
            ats.get(
                "keyword_score",
                0
            )
        ),
        (
            "Resume structure",
            structure_score
        ),
        (
            "Contact information",
            contact_score
        ),
        (
            "Resume length",
            length_score
        )
    ]

    st.markdown(
        '''
        <div class="panel">
            <div class="panel-title">ATS breakdown</div>
            <div class="panel-description">
                Performance across the main ATS factors.
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    for label, value in checks:
        val = max(
            0,
            min(
                float(value),
                100
            )
        )

        st.markdown(
            f'''
            <div style="display:flex;
            justify-content:space-between;
            font-size:12px;
            font-weight:600;
            color:#0F172A;
            margin-top:12px;
            margin-bottom:3px;">
                <span>{label}</span>
                <span>{val:.0f}%</span>
            </div>
            ''',
            unsafe_allow_html=True
        )

        st.progress(
            val / 100
        )


st.markdown(
    '<div class="section-header">'
    '<div class="section-title">Keyword analysis</div>'
    '<div class="section-description">'
    'Compare important keywords from the job description.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


keyword_data = ats.get(
    "keyword_analysis",
    {}
)


keyword_col1, keyword_col2, keyword_col3 = st.columns(
    3,
    gap="medium"
)


with keyword_col1:
    st.metric(
        "JD keywords",
        len(jd_skills)
    )


with keyword_col2:
    st.metric(
        "Matched",
        keyword_data.get(
            "match_count",
            0
        )
    )


with keyword_col3:
    st.metric(
        "Missing",
        keyword_data.get(
            "missing_count",
            0
        )
    )


keyword_left, keyword_right = st.columns(
    2,
    gap="medium"
)


with keyword_left:
    st.markdown(
        f'''
        <div class="panel">
            <div class="panel-title">
                Matched keywords
            </div>
            <div class="panel-description">
                Keywords already represented in the resume.
            </div>
            <div style="margin-top:10px;">
                {chips(
                    keyword_data.get("matched", []),
                    "chip-match"
                )}
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )


with keyword_right:
    st.markdown(
        f'''
        <div class="panel">
            <div class="panel-title">
                Missing keywords
            </div>
            <div class="panel-description">
                Relevant JD keywords not detected in the resume.
            </div>
            <div style="margin-top:10px;">
                {chips(
                    keyword_data.get("missing", []),
                    "chip-missing"
                )}
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )


st.markdown(
    '<div class="section-header">'
    '<div class="section-title">Resume quality checks</div>'
    '<div class="section-description">'
    'Basic structure, contact and content checks.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


structure_col, contact_col, length_col = st.columns(
    3,
    gap="medium"
)


with structure_col:
    structure_items = [
        (
            "Skills",
            sections.get(
                "Skills",
                False
            )
        ),
        (
            "Education",
            sections.get(
                "Education",
                False
            )
        ),
        (
            "Experience",
            sections.get(
                "Experience",
                False
            )
        ),
        (
            "Projects",
            sections.get(
                "Projects",
                False
            )
        )
    ]

    st.markdown(
        f'''
        <div class="panel">
            <div class="panel-title">
                Resume structure
            </div>
            <div class="panel-description">
                Important sections detected.
            </div>
            {status_rows(structure_items)}
        </div>
        ''',
        unsafe_allow_html=True
    )


with contact_col:
    contact_items = [
        (
            "Email",
            contact.get(
                "email",
                False
            )
        ),
        (
            "Phone",
            contact.get(
                "phone",
                False
            )
        ),
        (
            "LinkedIn",
            contact.get(
                "linkedin",
                False
            )
        ),
        (
            "GitHub",
            contact.get(
                "github",
                False
            )
        )
    ]

    st.markdown(
        f'''
        <div class="panel">
            <div class="panel-title">
                Contact information
            </div>
            <div class="panel-description">
                Professional profile details.
            </div>
            {status_rows(contact_items)}
        </div>
        ''',
        unsafe_allow_html=True
    )


with length_col:
    st.markdown(
        f'''
        <div class="panel">
            <div class="panel-title">
                Resume length
            </div>
            <div class="panel-description">
                Content word count evaluation.
            </div>
            <div class="metric-value">
                {length.get("word_count", 0)}
            </div>
            <div class="metric-label">
                WORDS
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    if length_status == "Good":
        st.success(
            "Recommended length.",
            icon="✅"
        )
    elif length_status == "Long":
        st.warning(
            "Consider reducing content.",
            icon="⚠️"
        )
    elif length_status == "Too short":
        st.warning(
            "Resume may need more detail.",
            icon="⚠️"
        )
    else:
        st.error(
            "Resume is very long.",
            icon="❗"
        )


st.markdown(
    '<div class="section-header">'
    '<div class="section-title">Recommended improvements</div>'
    '<div class="section-description">'
    'Practical changes based on the detected gaps.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


suggestions = result.get(
    "suggestions",
    []
)


if suggestions:
    for index, suggestion in enumerate(
        suggestions,
        start=1
    ):
        st.markdown(
            f'''
            <div class="alert-item">
                <div class="alert-title">
                    Recommendation {index}
                </div>
                {suggestion}
            </div>
            ''',
            unsafe_allow_html=True
        )
else:
    st.success(
        "No major improvement opportunities detected.",
        icon="✅"
    )


st.markdown(
    '''
    <div style="text-align:center;
    color:#94A3B8;
    font-size:11px;
    padding-top:40px;">
        ResumeMatch · Resume and job description analysis
    </div>
    ''',
    unsafe_allow_html=True
)
