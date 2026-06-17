import sys
import os
import io

# Allow importing from the same src/ directory
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from main import get_persona_reactions, get_web_search_summary, get_ats_score, get_career_coach_report, get_tailored_cv, get_cv_comparison, SYSTEM_PROMPT, ATS_SYSTEM_PROMPT

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CV Agent",
    page_icon="🚀",
    layout="wide",
)

# ── Custom CSS — dark theme ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Background */
.stApp { background-color: #0f1117; color: #c9cdd4; }

/* Hide default chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1180px; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.8rem 1rem 0.5rem 1rem;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
    margin: 0 0 0.6rem 0;
}
.hero p {
    font-size: 1.05rem;
    color: #7b7f9e;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}
.purple-divider {
    height: 3px;
    background: linear-gradient(90deg, transparent, #6c63ff, transparent);
    border: none;
    margin: 1.8rem auto;
    max-width: 160px;
    border-radius: 99px;
}

/* ── Cards ── */
.card {
    background: #1c1e26;
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid #252836;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    margin-bottom: 1rem;
}
.card-title {
    font-size: 1rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 1rem;
}
.upload-status-ok {
    background: #0d2e22;
    border: 1px solid #00c896;
    border-radius: 8px;
    padding: 0.5rem 0.8rem;
    color: #00c896;
    font-size: 0.85rem;
    font-weight: 500;
    margin-top: 0.6rem;
}
.upload-status-empty {
    background: #1c1e26;
    border: 1px dashed #3a3d52;
    border-radius: 8px;
    padding: 0.5rem 0.8rem;
    color: #5c6080;
    font-size: 0.85rem;
    margin-top: 0.6rem;
}

/* ── All buttons ── */
.stButton > button {
    background: #22253a !important;
    color: #a0a4be !important;
    border: 1px solid #2e3149 !important;
    border-radius: 8px !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover {
    background: #6c63ff !important;
    color: #ffffff !important;
    border-color: #6c63ff !important;
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(108,99,255,0.3) !important;
}

/* ── Primary CTA ── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #6c63ff, #8b5cf6) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    padding: 0.7rem 2rem !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 20px rgba(108,99,255,0.4) !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    opacity: 0.88 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(108,99,255,0.55) !important;
}

/* ── Text areas ── */
.stTextArea textarea {
    background: #13151f !important;
    color: #c9cdd4 !important;
    border: 1px solid #2a2d3a !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s ease !important;
}
.stTextArea textarea:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.15) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #13151f !important;
    border: 1px dashed #2e3149 !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #6c63ff !important;
}

/* ── Section heading ── */
.section-heading {
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0.2rem 0 1.2rem 0;
}
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, #6c63ff44, #6c63ffaa, #6c63ff44);
    border: none;
    margin: 2rem 0;
}

/* ── Persona cards ── */
.persona-card {
    background: #1c1e26;
    border-radius: 12px;
    padding: 1.3rem 1.3rem 1.3rem 1.5rem;
    border: 1px solid #252836;
    box-shadow: 0 4px 18px rgba(0,0,0,0.28);
    position: relative;
    margin-bottom: 1rem;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.persona-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}
.persona-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    border-radius: 12px 0 0 12px;
}
.pc-recruiter::before      { background: #00c896; }
.pc-hiring::before         { background: #6c63ff; }
.pc-coach::before          { background: #f4a261; }
.pc-expert::before         { background: #e05c5c; }

.pc-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.pc-recruiter .pc-label { color: #00c896; }
.pc-hiring    .pc-label { color: #6c63ff; }
.pc-coach     .pc-label { color: #f4a261; }
.pc-expert    .pc-label { color: #e05c5c; }

.pc-name {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.6rem;
}
.pc-text {
    font-size: 0.9rem;
    color: #9099b5;
    line-height: 1.65;
}

/* ── Insights card ── */
.insights-card {
    background: #1c1e26;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    border: 1px solid #252836;
    border-left: 4px solid #6c63ff;
    box-shadow: 0 4px 18px rgba(0,0,0,0.28);
    color: #9099b5;
    font-size: 0.93rem;
    line-height: 1.7;
}

/* ── Example label ── */
.ex-label {
    font-size: 0.75rem;
    color: #4a4e6a;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

/* ── ATS score section ── */
.ats-wrapper {
    background: #1c1e26;
    border-radius: 14px;
    padding: 2rem;
    border: 1px solid #252836;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    margin-bottom: 1rem;
    text-align: center;
}
.ats-score-value {
    font-size: 4rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.ats-score-label {
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #5c6080;
    margin-bottom: 1.6rem;
}
.ats-score-red    { color: #e05c5c; }
.ats-score-orange { color: #f4a261; }
.ats-score-green  { color: #00c896; }

.ats-sub-card {
    background: #13151f;
    border-radius: 10px;
    padding: 1rem 0.8rem;
    border: 1px solid #252836;
    text-align: center;
}
.ats-sub-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
}
.ats-sub-label {
    font-size: 0.72rem;
    color: #5c6080;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-top: 0.25rem;
}
.ats-explanation {
    background: #13151f;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    border: 1px solid #252836;
    color: #9099b5;
    font-size: 0.9rem;
    line-height: 1.65;
    margin-top: 1rem;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers: text extraction ───────────────────────────────────────────────────
def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        return "\n".join(
            page.extract_text() or "" for page in reader.pages
        ).strip()
    except Exception as e:
        st.error(f"Failed to read PDF: {e}")
        return ""


def extract_text_from_docx(file_bytes: bytes) -> str:
    try:
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip()).strip()
    except Exception as e:
        st.error(f"Failed to read DOCX: {e}")
        return ""


# ── Session state defaults ─────────────────────────────────────────────────────
for key, default in {
    "cv_text": "",
    "job_post_text": "",
    "results": None,
    "web_summary": None,
    "ats_result": None,
    "raw_ats_response": None,
    "coach_report": None,
    "raw_coach_response": None,
    "tailored_cv": None,
    "tailor_ats": None,
    "tailor_personas": None,
    "original_ats": None,
    "tailored_ats": None,
    "cv_comparison": None,
    "raw_personas": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Hero header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🚀 CV Agent</h1>
    <p>Upload your CV and paste a job description.<br>Get expert AI feedback instantly.</p>
</div>
<hr class="purple-divider"/>
""", unsafe_allow_html=True)

# ── Mode selector ─────────────────────────────────────────────────────────────
mode = st.radio("Choose mode:", ["🔍 Analyse CV", "✨ Tailor CV for Job"], horizontal=True)
st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

# ── Input columns ──────────────────────────────────────────────────────────────
col_cv, col_job = st.columns(2, gap="large")

# LEFT — CV Upload
with col_cv:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📄 Your CV</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        label="Upload CV",
        type=["pdf", "docx"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        if uploaded_file.name.lower().endswith(".pdf"):
            extracted = extract_text_from_pdf(file_bytes)
        else:
            extracted = extract_text_from_docx(file_bytes)

        if extracted:
            st.session_state.cv_text = extracted

        st.markdown(
            f'<div class="upload-status-ok">✅ CV uploaded: {uploaded_file.name}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="upload-status-empty">No file uploaded yet. We accept PDF and DOCX.</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT — Job Post
with col_job:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🏢 Job Post</div>', unsafe_allow_html=True)

    st.image(
        "https://placehold.co/600x180/1c1e26/6c63ff?text=Paste+the+Job+Description+Below",
        use_container_width=True,
    )

    st.text_area(
        label="Job Post",
        height=180,
        placeholder="Paste the full job description here...",
        label_visibility="collapsed",
        key="job_post_text",
    )

    st.markdown('<div class="ex-label">Quick examples</div>', unsafe_allow_html=True)
    ex_cols = st.columns(3)
    job_examples = [
        ("FinTech Backend Eng.", "Backend Engineer at FinTech Innovations – Python, FastAPI, SQL, AWS."),
        ("HealthAI Data Scientist", "Data Scientist at HealthAI – ML models, Python, pandas, NLP, healthcare."),
        ("EdTech Product Manager", "Product Manager at EdTech Startup – roadmap ownership, B2C SaaS."),
    ]

    def _set_job_example(txt: str):
        """Callback: runs before next render so the widget key can be updated."""
        st.session_state.job_post_text = txt

    for i, (label, text) in enumerate(job_examples):
        with ex_cols[i]:
            st.button(
                label,
                key=f"job_ex_{i}",
                use_container_width=True,
                on_click=_set_job_example,
                args=(text,),
            )

    st.markdown('</div>', unsafe_allow_html=True)

# ── CTA button ─────────────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
_btn_label = "🚀 Analyse My Application" if mode == "🔍 Analyse CV" else "✨ Tailor My CV"
analyse_clicked = st.button(
    _btn_label,
    type="primary",
    use_container_width=True,
)

# ── API calls ──────────────────────────────────────────────────────────────────
if analyse_clicked:
    cv_val  = st.session_state.cv_text.strip()
    job_val = st.session_state.job_post_text.strip()

    if not cv_val or not job_val:
        st.warning("⚠️ Please upload a CV and fill in the job description before analysing.")

    elif mode == "✨ Tailor CV for Job":
        # ── Tailor mode pipeline ────────────────────────────────────────────────
        # Step 1: Original ATS score
        try:
            with st.spinner("Calculating original ATS score…"):
                original_ats, _ = get_ats_score(cv_val, job_val)
            st.session_state.original_ats = original_ats
        except Exception as e:
            st.error(f"Original ATS scoring failed: {e}")
            st.session_state.original_ats = None

        # Step 2: generate tailored CV
        tailored_text = None
        try:
            with st.spinner("Tailoring your CV for this role…"):
                tailored_text, _ = get_tailored_cv(cv_val, job_val)
            st.session_state.tailored_cv = tailored_text
        except Exception as e:
            st.error(f"CV tailoring failed: {e}")
            st.session_state.tailored_cv = None

        if tailored_text:
            # Step 3: ATS score on tailored CV
            try:
                with st.spinner("Calculating ATS score for tailored CV…"):
                    tailor_ats, _ = get_ats_score(tailored_text, job_val)
                st.session_state.tailored_ats = tailor_ats
                st.session_state.tailor_ats = tailor_ats
            except Exception as e:
                st.error(f"Tailored ATS scoring failed: {e}")
                st.session_state.tailored_ats = None
                st.session_state.tailor_ats = None

            # Step 4: persona reactions on tailored CV
            try:
                with st.spinner("Running expert panel on tailored CV…"):
                    tailor_personas, raw_personas = get_persona_reactions(tailored_text, job_val)
                st.session_state.tailor_personas = tailor_personas
                st.session_state.raw_personas = raw_personas
            except Exception as e:
                st.error(f"Expert panel failed: {e}")
                st.session_state.tailor_personas = None
                st.session_state.raw_personas = None

            # Step 5: CV comparison
            try:
                with st.spinner("Comparing CVs…"):
                    cv_comparison, _ = get_cv_comparison(cv_val, tailored_text, job_val)
                st.session_state.cv_comparison = cv_comparison
            except Exception as e:
                st.error(f"CV comparison failed: {e}")
                st.session_state.cv_comparison = None

    else:
        # ── Analyse mode pipeline ───────────────────────────────────────────────
        # ATS score (first)
        try:
            with st.spinner("Calculating ATS score…"):
                ats, raw_ats = get_ats_score(cv_val, job_val)
            st.session_state.ats_result = ats
            st.session_state.original_ats = ats
            st.session_state.raw_ats_response = raw_ats
        except Exception as e:
            st.error(f"ATS scoring failed: {e}")
            st.session_state.ats_result = None
            st.session_state.original_ats = None

        # Persona reactions
        try:
            with st.spinner("Analysing your application with four expert lenses…"):
                personas, raw_personas = get_persona_reactions(cv_val, job_val)
            st.session_state.results = personas
            st.session_state.raw_personas = raw_personas
        except Exception as e:
            st.error(f"Failed to get persona reactions: {e}")
            st.session_state.results = None
            st.session_state.raw_personas = None

        # Web search
        if st.session_state.results:
            try:
                with st.spinner("Searching the web for company insights…"):
                    summary = get_web_search_summary(job_val)
                st.session_state.web_summary = summary
            except Exception as e:
                st.error(f"Web search failed: {e}")
                st.session_state.web_summary = None

        # Career coach report
        try:
            with st.spinner("Generating Career Coach report…"):
                report, raw_coach = get_career_coach_report(cv_val, job_val)
            st.session_state.coach_report = report
            st.session_state.raw_coach_response = raw_coach
        except Exception as e:
            st.error(f"Career coach report failed: {e}")
            st.session_state.coach_report = None
            st.session_state.raw_coach_response = None

# ── Results ────────────────────────────────────────────────────────────────────
if st.session_state.ats_result or st.session_state.results:

    # ── ATS Score section ──────────────────────────────────────────────────────
    if st.session_state.ats_result:
        ats = st.session_state.ats_result
        overall = ats.get("overall_score", 0)

        if overall >= 75:
            score_color_cls = "ats-score-green"
            score_hex = "#00c896"
        elif overall >= 50:
            score_color_cls = "ats-score-orange"
            score_hex = "#f4a261"
        else:
            score_color_cls = "ats-score-red"
            score_hex = "#e05c5c"

        st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">📊 ATS Compatibility Score</div>', unsafe_allow_html=True)

        # Centered overall score
        _, score_col, _ = st.columns([1, 2, 1])
        with score_col:
            st.markdown(f"""
            <div class="ats-wrapper">
                <div class="ats-score-value {score_color_cls}">{overall}</div>
                <div class="ats-score-label">ATS Score / 100</div>
            </div>
            """, unsafe_allow_html=True)

        # Four sub-metrics in one row
        m1, m2, m3, m4 = st.columns(4, gap="small")
        sub_metrics = [
            (m1, "Skill Match",          ats.get("skill_match", 0)),
            (m2, "Experience",           ats.get("experience_alignment", 0)),
            (m3, "Keyword Coverage",     ats.get("keyword_coverage", 0)),
            (m4, "Education Relevance",  ats.get("education_relevance", 0)),
        ]
        for col, label, val in sub_metrics:
            with col:
                st.markdown(f"""
                <div class="ats-sub-card">
                    <div class="ats-sub-value">{val}<span style="font-size:1rem;color:#5c6080">/100</span></div>
                    <div class="ats-sub-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        # Explanation
        explanation = ats.get("explanation", "")
        if explanation:
            st.markdown(f'<div class="ats-explanation">{explanation}</div>', unsafe_allow_html=True)

if st.session_state.results:
    personas = st.session_state.results

    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">👥 Expert Panel</div>', unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2, gap="large")
    r2c1, r2c2 = st.columns(2, gap="large")

    def persona_card(col, css_cls: str, label: str, name: str, key: str):
        text = personas.get(key, "No response.")
        with col:
            st.markdown(f"""
            <div class="persona-card {css_cls}">
                <div class="pc-label">{label}</div>
                <div class="pc-name">{name}</div>
                <div class="pc-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    persona_card(r1c1, "pc-recruiter", "🟢 Recruiter",        "Recruiter",        "recruiter")
    persona_card(r1c2, "pc-hiring",    "🔵 Hiring Manager",   "Hiring Manager",   "hiring_manager")
    persona_card(r2c1, "pc-coach",     "🟡 Career Coach",     "Career Coach",     "career_coach")
    persona_card(r2c2, "pc-expert",    "🔴 Industry Expert",  "Industry Expert",  "industry_expert")

    # ── Web insights ───────────────────────────────────────────────────────────
    if st.session_state.web_summary is not None:
        st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">🌐 Company & Role Insights</div>', unsafe_allow_html=True)

        insight_text = st.session_state.web_summary or "No relevant company information found."
        st.markdown(f'<div class="insights-card">{insight_text}</div>', unsafe_allow_html=True)

    # ── Career Coach Report ────────────────────────────────────────────────────
    if st.session_state.coach_report:
        st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">🎯 Career Coach Report</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(st.session_state.coach_report)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Career Coach Report",
            data=st.session_state.coach_report,
            file_name="career_coach_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # ── Reset ──────────────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("🔄  Try Another Application", use_container_width=True):
            st.session_state.cv_text            = ""
            st.session_state.job_post_text      = ""
            st.session_state.results            = None
            st.session_state.web_summary        = None
            st.session_state.ats_result         = None
            st.session_state.raw_ats_response   = None
            st.session_state.coach_report       = None
            st.session_state.raw_coach_response = None
            st.session_state.tailored_cv        = None
            st.session_state.tailor_ats         = None
            st.session_state.tailor_personas    = None
            st.session_state.original_ats       = None
            st.session_state.tailored_ats       = None
            st.session_state.cv_comparison      = None
            st.session_state.raw_personas       = None
            st.rerun()

# ── Tailor mode results ────────────────────────────────────────────────────────
if st.session_state.tailored_cv:
    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">✨ Your Tailored CV</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(st.session_state.tailored_cv)
    st.markdown('</div>', unsafe_allow_html=True)
    st.download_button(
        label="📥 Download Tailored CV",
        data=st.session_state.tailored_cv,
        file_name="tailored_cv.md",
        mime="text/markdown",
        use_container_width=True,
    )

    # ATS score for tailored CV
    if st.session_state.tailored_ats:
        tats = st.session_state.tailored_ats
        t_overall = tats.get("overall_score", 0)
        t_cls = "ats-score-green" if t_overall >= 75 else ("ats-score-orange" if t_overall >= 50 else "ats-score-red")

        st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">📊 Tailored CV ATS Score</div>', unsafe_allow_html=True)
        _, sc, _ = st.columns([1, 2, 1])
        with sc:
            st.markdown(f"""
            <div class="ats-wrapper">
                <div class="ats-score-value {t_cls}">{t_overall}</div>
                <div class="ats-score-label">ATS Score / 100</div>
            </div>""", unsafe_allow_html=True)
        tm1, tm2, tm3, tm4 = st.columns(4, gap="small")
        for col, lbl, val in [
            (tm1, "Skill Match",         tats.get("skill_match", 0)),
            (tm2, "Experience",          tats.get("experience_alignment", 0)),
            (tm3, "Keyword Coverage",    tats.get("keyword_coverage", 0)),
            (tm4, "Education Relevance", tats.get("education_relevance", 0)),
        ]:
            with col:
                st.markdown(f"""
                <div class="ats-sub-card">
                    <div class="ats-sub-value">{val}<span style="font-size:1rem;color:#5c6080">/100</span></div>
                    <div class="ats-sub-label">{lbl}</div>
                </div>""", unsafe_allow_html=True)
        texpl = tats.get("explanation", "")
        if texpl:
            st.markdown(f'<div class="ats-explanation">{texpl}</div>', unsafe_allow_html=True)

    # Expert panel for tailored CV
    if st.session_state.tailor_personas:
        tp = st.session_state.tailor_personas
        st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">👥 Expert Panel — Tailored CV</div>', unsafe_allow_html=True)
        tr1c1, tr1c2 = st.columns(2, gap="large")
        tr2c1, tr2c2 = st.columns(2, gap="large")
        def tailor_persona_card(col, css_cls, label, name, key):
            text = tp.get(key, "No response.")
            with col:
                st.markdown(f"""
                <div class="persona-card {css_cls}">
                    <div class="pc-label">{label}</div>
                    <div class="pc-name">{name}</div>
                    <div class="pc-text">{text}</div>
                </div>""", unsafe_allow_html=True)
        tailor_persona_card(tr1c1, "pc-recruiter", "🟢 Recruiter",       "Recruiter",       "recruiter")
        tailor_persona_card(tr1c2, "pc-hiring",    "🔵 Hiring Manager",  "Hiring Manager",  "hiring_manager")
        tailor_persona_card(tr2c1, "pc-coach",     "🟡 Career Coach",    "Career Coach",    "career_coach")
        tailor_persona_card(tr2c2, "pc-expert",    "🔴 Industry Expert", "Industry Expert", "industry_expert")

    # COMPARISON SECTION
    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📊 Original vs Tailored CV — Comparison</div>', unsafe_allow_html=True)

    # 1. ATS Score Comparison
    orig_score = st.session_state.original_ats.get("overall_score", 0) if st.session_state.original_ats else 0
    tail_score = st.session_state.tailored_ats.get("overall_score", 0) if st.session_state.tailored_ats else 0
    diff = tail_score - orig_score

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="Original ATS Score", value=f"{orig_score}/100")
    with m_col2:
        st.metric(label="Tailored ATS Score", value=f"{tail_score}/100")
    with m_col3:
        delta_val = f"+{diff} points" if diff >= 0 else f"{diff} points"
        st.metric(
            label="Improvement",
            value=delta_val,
            delta=diff if diff != 0 else None,
            delta_color="normal"
        )

    # 2. Side-by-Side CV Text
    col_orig_text, col_tail_text = st.columns(2)
    with col_orig_text:
        st.markdown("##### 📄 Original CV")
        st.text_area(
            label="Original CV Text",
            value=st.session_state.cv_text,
            height=400,
            disabled=True,
            label_visibility="collapsed",
            key="compare_original_cv_text_area"
        )
    with col_tail_text:
        st.markdown("##### ✨ Tailored CV")
        st.text_area(
            label="Tailored CV Text",
            value=st.session_state.tailored_cv,
            height=400,
            disabled=True,
            label_visibility="collapsed",
            key="compare_tailored_cv_text_area"
        )

    # 3. What Changed — Keyword Analysis
    if st.session_state.cv_comparison:
        comp = st.session_state.cv_comparison
        summary_text = comp.get("summary", "")
        if summary_text:
            st.markdown(f"<div style='margin-top:1.5rem; margin-bottom:1rem;'><strong>Summary:</strong> {summary_text}</div>", unsafe_allow_html=True)

        with st.expander("🔑 Added Keywords"):
            keywords = comp.get("added_keywords", [])
            if keywords:
                st.markdown("\n".join(f"- {kw}" for kw in keywords))
            else:
                st.write("No keywords added.")

        with st.expander("📈 Improved Sections"):
            sections = comp.get("improved_sections", [])
            if sections:
                st.markdown("\n".join(f"- {sec}" for sec in sections))
            else:
                st.write("No sections improved.")

        with st.expander("✅ Missing Skills Now Addressed"):
            skills = comp.get("skills_addressed", [])
            if skills:
                st.markdown("\n".join(f"- {sk}" for sk in skills))
            else:
                st.write("No missing skills addressed.")

        with st.expander("💬 Stronger Wording Examples"):
            wording = comp.get("stronger_wording", [])
            if wording:
                st.markdown("\n".join(f"- {w}" for w in wording))
            else:
                st.write("No wording improvements.")

    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
    _, tmid, _ = st.columns([1, 2, 1])
    with tmid:
        if st.button("🔄  Start Over", key="tailor_reset", use_container_width=True):
            st.session_state.tailored_cv     = None
            st.session_state.tailor_ats      = None
            st.session_state.tailor_personas = None
            st.session_state.original_ats    = None
            st.session_state.tailored_ats    = None
            st.session_state.cv_comparison   = None
            st.rerun()

# ── Teach Mode Section ────────────────────────────────────────────────────────
st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">🎓 Teach Mode</div>', unsafe_allow_html=True)

with st.expander("System Prompt"):
    st.code(SYSTEM_PROMPT)

with st.expander("Raw JSON"):
    st.code(st.session_state.raw_personas or "No raw JSON response recorded yet.")

with st.expander("Search Request"):
    search_prompt = (
        f"Based on your training knowledge, provide a brief background on the company and role described here: {st.session_state.job_post_text or '<job_post>'}.\n"
        "Summarize in 3-4 sentences: what the company or industry is known for, what kind of candidates "
        "succeed in this type of role, and any relevant context useful to someone preparing to apply. "
        "If you have no specific knowledge of the company, provide useful industry context instead."
    )
    st.code(search_prompt)

with st.expander("ATS Scoring prompt"):
    st.code(ATS_SYSTEM_PROMPT)
