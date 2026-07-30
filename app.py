import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
import json
import re


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found. Please create a .env file.")
    st.stop()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-3.6-flash")


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .score-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    }

    .score {
        font-size: 48px;
        font-weight: bold;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume and discover how well it matches your target job role.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# RESUME TEXT EXTRACTION
# --------------------------------------------------

def extract_resume_text(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# --------------------------------------------------
# AI ANALYSIS FUNCTION
# --------------------------------------------------

def analyze_resume(resume_text, job_role):

    prompt = f"""
You are an expert technical recruiter and resume evaluator.

Analyze the following resume for the target job role:

TARGET JOB ROLE:
{job_role}

RESUME:
{resume_text}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "score": 0,
    "skills": [],
    "keywords": [],
    "missing_keywords": [],
    "strengths": [],
    "weaknesses": [],
    "suggestions": []
}}

Instructions:

1. score:
Give a resume-job match score from 0 to 100.

2. skills:
List the important technical and professional skills found in the resume.

3. keywords:
List important job-related keywords already present in the resume.

4. missing_keywords:
List important keywords or skills expected for the target role but missing from the resume.

5. strengths:
List strong points of the resume.

6. weaknesses:
List areas that could be improved.

7. suggestions:
Give practical suggestions for improving the resume for the target role.

Do not invent experience that is not present in the resume.
"""


    try:

        response = model.generate_content(prompt)

        response_text = response.text.strip()

        # Remove markdown code fences if Gemini adds them
        response_text = re.sub(
            r"^```json\s*",
            "",
            response_text,
            flags=re.IGNORECASE
        )

        response_text = re.sub(
            r"^```\s*",
            "",
            response_text
        )

        response_text = re.sub(
            r"\s*```$",
            "",
            response_text
        )

        result = json.loads(response_text)

        return result

    except json.JSONDecodeError:

        st.error("The AI returned an unexpected response format.")

        st.code(response.text)

        return None

    except Exception as e:

        st.error(f"AI analysis failed: {e}")

        return None


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    st.write(
        "Upload your resume and select the job role "
        "you want to analyze it against."
    )

    st.info(
        "Supported format: PDF"
    )


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.header("1️⃣ Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"]
)


st.header("2️⃣ Target Job Role")

job_role = st.text_input(
    "Enter the job role",
    placeholder="Example: Data Scientist"
)


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.button(
    "🚀 Analyze Resume",
    use_container_width=True
):

    if uploaded_file is None:

        st.warning("Please upload your resume first.")

    elif not job_role.strip():

        st.warning("Please enter a target job role.")

    else:

        with st.spinner("Reading and analyzing your resume..."):

            try:

                resume_text = extract_resume_text(uploaded_file)

                if not resume_text.strip():

                    st.error(
                        "Could not extract text from this PDF. "
                        "Please upload a text-based PDF resume."
                    )

                else:

                    result = analyze_resume(
                        resume_text,
                        job_role
                    )

                    if result:

                        st.session_state["analysis"] = result
                        st.session_state["resume_text"] = resume_text
                        st.session_state["job_role"] = job_role

                        st.success(
                            "Resume analysis completed successfully!"
                        )

            except Exception as e:

                st.error(
                    f"Could not process the resume: {e}"
                )


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if "analysis" in st.session_state:

    result = st.session_state["analysis"]

    st.divider()

    st.header("📊 Resume Analysis")

    # SCORE
    score = result.get("score", 0)

    col1, col2, col3 = st.columns(3)

    with col2:

        st.markdown(
            f"""
            <div class="score-box">
                <div>Resume Match Score</div>
                <div class="score">{score}/100</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # SKILLS
    st.markdown(
        '<div class="section-title">🛠️ Skills Found</div>',
        unsafe_allow_html=True
    )

    skills = result.get("skills", [])

    if skills:

        st.write(" • ".join(skills))

    else:

        st.write("No skills identified.")


    # KEYWORDS
    st.markdown(
        '<div class="section-title">🔑 Keywords Found</div>',
        unsafe_allow_html=True
    )

    keywords = result.get("keywords", [])

    if keywords:

        for keyword in keywords:

            st.write(f"✅ {keyword}")

    else:

        st.write("No major keywords identified.")


    # MISSING KEYWORDS
    st.markdown(
        '<div class="section-title">⚠️ Missing Keywords</div>',
        unsafe_allow_html=True
    )

    missing_keywords = result.get(
        "missing_keywords",
        []
    )

    if missing_keywords:

        for keyword in missing_keywords:

            st.write(f"❌ {keyword}")

    else:

        st.write(
            "No major missing keywords identified."
        )


    # STRENGTHS
    st.markdown(
        '<div class="section-title">💪 Strengths</div>',
        unsafe_allow_html=True
    )

    strengths = result.get("strengths", [])

    for strength in strengths:

        st.write(f"✅ {strength}")


    # WEAKNESSES
    st.markdown(
        '<div class="section-title">🔧 Weaknesses</div>',
        unsafe_allow_html=True
    )

    weaknesses = result.get("weaknesses", [])

    for weakness in weaknesses:

        st.write(f"⚠️ {weakness}")


    # SUGGESTIONS
    st.markdown(
        '<div class="section-title">🤖 AI Improvement Suggestions</div>',
        unsafe_allow_html=True
    )

    suggestions = result.get("suggestions", [])

    for suggestion in suggestions:

        st.write(f"💡 {suggestion}")


    # DOWNLOAD REPORT
    st.divider()

    report = f"""
AI RESUME ANALYZER REPORT

Target Job Role:
{st.session_state["job_role"]}

Resume Match Score:
{score}/100

SKILLS FOUND:
{chr(10).join("- " + str(x) for x in skills)}

KEYWORDS FOUND:
{chr(10).join("- " + str(x) for x in keywords)}

MISSING KEYWORDS:
{chr(10).join("- " + str(x) for x in missing_keywords)}

STRENGTHS:
{chr(10).join("- " + str(x) for x in strengths)}

WEAKNESSES:
{chr(10).join("- " + str(x) for x in weaknesses)}

AI SUGGESTIONS:
{chr(10).join("- " + str(x) for x in suggestions)}
"""

    st.download_button(
        label="📥 Download Analysis Report",
        data=report,
        file_name="resume_analysis_report.txt",
        mime="text/plain",
        use_container_width=True
    )