import streamlit as st
import fitz  # PyMuPDF
import re

# Known technical skills (extendable)
KNOWN_SKILLS = [
    "Python", "Java", "C++", "SQL", "JavaScript", "HTML", "CSS",
    "React", "Node.js", "Django", "Flask", "Git", "GitHub", "AWS",
    "Linux", "MongoDB", "PostgreSQL", "REST", "Agile"
]

# --------- Utility Functions ---------

def extract_text(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    return "".join(page.get_text() for page in doc)

def extract_skills(text):
    return [skill for skill in KNOWN_SKILLS if re.search(rf"\b{skill}\b", text, re.IGNORECASE)]

def extract_job_keywords(jd_text):
    return [skill for skill in KNOWN_SKILLS if re.search(rf"\b{skill}\b", jd_text, re.IGNORECASE)]

def match_skills(resume_skills, job_skills):
    matched = [s for s in job_skills if s in resume_skills]
    missing = [s for s in job_skills if s not in resume_skills]
    return matched, missing

def calculate_match_score(matched, total_required):
    return round((len(matched) / total_required) * 100, 2) if total_required else 0

# --------- Streamlit UI ---------

st.set_page_config(page_title="Resume Analyzer", page_icon="📝", layout="centered")

st.title("📄 AI Resume Analyzer")
st.caption("Upload your resume and paste the job description to see how well you match!")

resume_file = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("📝 Paste Job Description here", height=200)

if resume_file and job_description:
    if st.button("🔍 Analyze Resume"):

        # Extract and process
        resume_text = extract_text(resume_file)
        resume_skills = extract_skills(resume_text)
        job_skills = extract_job_keywords(job_description)
        matched, missing = match_skills(resume_skills, job_skills)
        score = calculate_match_score(matched, len(job_skills))

        # 🧾 Resume Summary
        st.header("📑 Resume Summary")
        st.markdown(f"- **File Name**: `{resume_file.name}`")
        st.markdown(f"- **Total Extracted Skills**: `{len(resume_skills)}`")
        st.markdown(f"- **Preview Text:**")
        st.write(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)

        # 📊 Match Score
        st.header("📊 Skill Match Score")
        st.progress(score / 100)
        st.markdown(f"**Match Score: {score}%**")

        # ✅ Matched Skills
        st.success("✅ Matched Skills:")
        st.write(matched or "No matched skills found.")

        # ❌ Missing Skills
        st.error("❌ Missing (Required) Skills:")
        st.write(missing or "None! You're a perfect match.")

        # 💡 Suggestions
        st.header("💡 Suggestions to Improve")
        if not missing:
            st.info("You're a great match! Just make sure your resume highlights these skills clearly.")
        else:
            st.warning("Consider adding these missing skills or projects that demonstrate them.")

else:
    st.info("Please upload your resume and paste a job description to begin analysis.")
