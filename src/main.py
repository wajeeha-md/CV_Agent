import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Hardcoded test strings
TEST_CV = "Software Engineer, 3 years experience, Python/Django, PostgreSQL, Docker. BSc CS."
TEST_JOB_POST = "Backend Engineer at FinTech Innovations. Requires Python, FastAPI, SQL, AWS."

SYSTEM_PROMPT = (
    "You are a panel of four expert personas evaluating a job application. "
    "You must respond ONLY with a valid JSON object with exactly these four keys: "
    "recruiter, hiring_manager, career_coach, industry_expert. "
    "Each key's value is a string of 2-3 sentences giving that persona's honest reaction. "
    "The recruiter focuses on whether the CV passes ATS screening filters and keyword matching. "
    "The hiring_manager assesses culture fit, ownership mindset, and team readiness. "
    "The career_coach gives specific advice on how to better position the candidate for this role. "
    "The industry_expert evaluates the technical depth and relevance to the job's domain. "
    "Return only the JSON. No markdown, no backticks, no extra text."
)


def _get_client() -> OpenAI:
    """Initialise and return an OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not found in .env")
    return OpenAI(api_key=api_key)


def get_persona_reactions(cv: str, job_post: str) -> tuple[dict, str]:
    """
    Call gpt-4o and return a tuple of:
      - parsed dict with keys: recruiter, hiring_manager, career_coach, industry_expert
      - the raw JSON string returned by the model (before json.loads)
    Raises on API or parse failure.
    """
    client = _get_client()
    user_message = f"CV:\n{cv}\n\nJob Post:\n{job_post}"

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    raw_json = response.choices[0].message.content
    personas = json.loads(raw_json)
    return personas, raw_json


def get_web_search_summary(job_post: str) -> str:
    """
    Use gpt-4o to generate a concise company/role background summary.
    Returns the summary string, or an empty string if nothing was found.
    Raises on API failure.
    """
    client = _get_client()
    user_message = (
        f"Based on your training knowledge, provide a brief background on the company and role described here: {job_post}. "
        "Summarize in 3-4 sentences: what the company or industry is known for, what kind of candidates "
        "succeed in this type of role, and any relevant context useful to someone preparing to apply. "
        "If you have no specific knowledge of the company, provide useful industry context instead."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": user_message},
        ],
    )

    content = response.choices[0].message.content
    return content.strip() if content else ""


ATS_SYSTEM_PROMPT = (
    "You are an ATS (Applicant Tracking System) evaluator. "
    "Analyze the CV against the job description and respond ONLY with a valid JSON object "
    "with exactly these keys: "
    "overall_score: an integer from 0 to 100, "
    "skill_match: an integer from 0 to 100, "
    "experience_alignment: an integer from 0 to 100, "
    "keyword_coverage: an integer from 0 to 100, "
    "education_relevance: an integer from 0 to 100, "
    "explanation: a string of 3-4 sentences explaining the overall score and the main "
    "reasons the candidate did or did not score well. "
    "Return only the JSON. No markdown, no backticks, no extra text."
)


def get_ats_score(cv: str, job_post: str) -> tuple[dict, str]:
    """
    Call gpt-4o and return a tuple of:
      - parsed dict with keys: overall_score, skill_match, experience_alignment,
        keyword_coverage, education_relevance, explanation
      - the raw JSON string returned by the model (before json.loads)
    Raises a clear exception on API or parse failure.
    """
    client = _get_client()
    user_message = f"CV:\n{cv}\n\nJob Post:\n{job_post}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": ATS_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        raw_json = response.choices[0].message.content
        ats = json.loads(raw_json)
        return ats, raw_json
    except json.JSONDecodeError as e:
        raise ValueError(f"ATS response was not valid JSON: {e}") from e
    except Exception as e:
        raise RuntimeError(f"ATS API call failed: {e}") from e



CAREER_COACH_SYSTEM_PROMPT = (
    "You are an expert career coach and professional CV writer. "
    "Analyze the CV against the job description and produce a structured improvement report "
    "in clean markdown format with exactly these sections in this order:\n\n"
    "## Suggested Skills to Add\n"
    "A bullet list of specific skills missing from the CV that appear in the job description.\n\n"
    "## Improved Experience Descriptions\n"
    "Rewritten versions of the candidate's existing experience bullet points using stronger "
    "action verbs and quantified achievements where possible. Use only information present "
    "in the original CV — do not fabricate details.\n\n"
    "## Improved Project Descriptions\n"
    "Rewritten versions of the candidate's existing project descriptions, optimized for "
    "impact and relevance to the target role.\n\n"
    "## Resume Wording Improvements\n"
    "A bullet list of specific wording changes: show the original phrase and the improved version "
    "in the format: original → improved\n\n"
    "## Missing Sections\n"
    "A bullet list of CV sections that are absent but would strengthen this application "
    "(e.g. GitHub link, certifications, metrics, summary statement).\n\n"
    "Write only what can be supported by the original CV. Do not invent experience, skills, "
    "education, or projects."
)


def get_career_coach_report(cv: str, job_post: str) -> tuple[str, str]:
    """
    Call gpt-4o and return a tuple of:
      - full structured markdown report string
      - the same raw string (identical, for consistency with other functions)
    Raises a clear exception on API failure.
    """
    client = _get_client()
    user_message = f"CV:\n{cv}\n\nJob Post:\n{job_post}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": CAREER_COACH_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        raw = response.choices[0].message.content or ""
        return raw.strip(), raw.strip()
    except Exception as e:
        raise RuntimeError(f"Career coach API call failed: {e}") from e


TAILOR_CV_SYSTEM_PROMPT = (
    "You are an expert CV writer and career strategist.\n"
    "Your task is to rewrite and restructure the provided CV to maximize its relevance\n"
    "for the target job description.\n\n"
    "Rules you must follow:\n"
    "- Use only information present in the original CV. Do not fabricate any experience,\n"
    "  skills, education, certifications, projects, or achievements.\n"
    "- Reorder sections to prioritize what is most relevant to the target role.\n"
    "- Rewrite bullet points using strong action verbs and quantified impact where\n"
    "  the original CV supports it.\n"
    "- Add a tailored professional summary at the top optimized for the role.\n"
    "- Incorporate keywords from the job description naturally throughout the CV.\n"
    "- Reduce emphasis on experience and skills that are irrelevant to the target role.\n"
    "- Output the full rewritten CV in clean markdown format, ready to be copied and used.\n\n"
    "Structure the output CV with these sections in order (include only sections that\n"
    "exist in the original CV):\n"
    "# [Candidate Name]\n"
    "[Contact info if present]\n\n"
    "## Professional Summary\n"
    "## Skills\n"
    "## Experience\n"
    "## Projects (if present)\n"
    "## Education\n"
    "## Certifications (if present)\n"
    "## Achievements (if present)"
)


def get_tailored_cv(cv: str, job_post: str) -> tuple[str, str]:
    """
    Rewrite the CV targeting the given job post.
    Returns (tailored_markdown, raw_string).
    Raises RuntimeError on API failure.
    """
    client = _get_client()
    user_message = f"Original CV:\n{cv}\n\nTarget Job Post:\n{job_post}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": TAILOR_CV_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        raw = response.choices[0].message.content or ""
        return raw.strip(), raw.strip()
    except Exception as e:
        raise RuntimeError(f"CV tailoring API call failed: {e}") from e


CV_COMPARISON_SYSTEM_PROMPT = (
    "You are a CV analyst. Compare the original and tailored CV against the job description.\n"
    "Respond ONLY with a valid JSON object with exactly these keys:\n"
    "added_keywords: a list of strings — keywords present in the tailored CV but not the original\n"
    "improved_sections: a list of strings — sections that were strengthened or reordered\n"
    "skills_addressed: a list of strings — missing skills from the original that now appear\n"
    "stronger_wording: a list of strings — examples of improved phrasing in format 'old → new'\n"
    "summary: a string of 2-3 sentences summarising the overall improvement\n"
    "Return only the JSON. No markdown, no backticks, no extra text."
)


def get_cv_comparison(original_cv: str, tailored_cv: str, job_post: str) -> tuple[dict, str]:
    """
    Call gpt-4o and return a tuple of:
      - parsed dict comparison results
      - the raw JSON string returned by the model
    Raises a clear exception on API or parse failure.
    """
    client = _get_client()
    user_message = f"Original CV:\n{original_cv}\n\nTailored CV:\n{tailored_cv}\n\nJob Post:\n{job_post}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": CV_COMPARISON_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        raw_json = response.choices[0].message.content or ""
        comparison = json.loads(raw_json)
        return comparison, raw_json
    except json.JSONDecodeError as e:
        raise ValueError(f"CV comparison response was not valid JSON: {e}") from e
    except Exception as e:
        raise RuntimeError(f"CV comparison API call failed: {e}") from e



# ── Standalone runner ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")

    def safe_print(text: str):
        import sys
        try:
            print(text)
        except UnicodeEncodeError:
            enc = sys.stdout.encoding or 'utf-8'
            print(text.encode(enc, errors='replace').decode(enc))

    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in .env")
    else:
        print("Project scaffold ready. API key loaded.")

        # ATS score
        try:
            ats, _ = get_ats_score(TEST_CV, TEST_JOB_POST)
            print("\n" + "=" * 60)
            print("ATS COMPATIBILITY SCORE")
            print("=" * 60)
            print(f"\nATS SCORE: {ats['overall_score']}/100")
            print(f"Skill Match: {ats['skill_match']} | Experience: {ats['experience_alignment']} | Keywords: {ats['keyword_coverage']} | Education: {ats['education_relevance']}")
            safe_print(f"\nEXPLANATION: {ats['explanation']}")
            print("\n" + "=" * 60)
        except Exception as e:
            print(f"ERROR: ATS scoring failed — {e}")

        # Persona reactions
        try:
            personas, _ = get_persona_reactions(TEST_CV, TEST_JOB_POST)
            print("\n" + "=" * 60)
            print("CV EVALUATION — EXPERT PANEL REPORT")
            print("=" * 60)
            safe_print(f"\nRECRUITER:\n{personas['recruiter']}")
            safe_print(f"\nHIRING MANAGER:\n{personas['hiring_manager']}")
            safe_print(f"\nCAREER COACH:\n{personas['career_coach']}")
            safe_print(f"\nINDUSTRY EXPERT:\n{personas['industry_expert']}")
            print("\n" + "=" * 60)
        except json.JSONDecodeError as e:
            print(f"ERROR: Failed to parse JSON response — {e}")
        except Exception as e:
            print(f"ERROR: API call failed — {e}")

        # Web search summary
        try:
            summary = get_web_search_summary(TEST_JOB_POST)
            print("\n" + "=" * 60)
            print("COMPANY & ROLE INSIGHTS FROM THE WEB")
            print("=" * 60)
            safe_print(f"\n{summary}" if summary else "No relevant company information found.")
            print("\n" + "=" * 60)
        except Exception as e:
            print("\n" + "=" * 60)
            print("COMPANY & ROLE INSIGHTS FROM THE WEB")
            print("=" * 60)
            print(f"Web search unavailable: {e}")
            print("\n" + "=" * 60)

        # Career coach report
        try:
            report, _ = get_career_coach_report(TEST_CV, TEST_JOB_POST)
            print("CAREER COACH REPORT:")
            safe_print(report)
        except Exception as e:
            print(f"ERROR: Career coach report failed — {e}")

        # Tailored CV
        try:
            tailored, _ = get_tailored_cv(TEST_CV, TEST_JOB_POST)
            print("\n" + "=" * 60)
            print("TAILORED CV")
            print("=" * 60)
            safe_print(f"\n{tailored}")
            print("\n" + "=" * 60)
        except Exception as e:
            print(f"ERROR: CV tailoring failed — {e}")
