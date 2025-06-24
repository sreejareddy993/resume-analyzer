import streamlit as st
import openai
import pdfplumber

st.title("🧠 AI-Powered Resume Analyzer")

st.write("Upload your resume PDF and a job description. Get AI-powered feedback!")

# 🗝️ Ask user for OpenAI API Key
user_api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")

if not user_api_key:
    st.warning("⚠️ Please enter your OpenAI API key to use the app.")
    st.stop()

# Create OpenAI client
client = openai.OpenAI(api_key=user_api_key)

# Upload resume
resume_file = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])

# Paste job description
job_desc = st.text_area("📝 Paste Job Description")

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Analyze
if st.button("Analyze"):
    if resume_file and job_desc.strip():
        st.info("⏳ Extracting resume text...")
        try:
            resume_text = extract_text_from_pdf(resume_file)
        except Exception as e:
            st.error(f"❌ Couldn't read the resume: {e}")
            st.stop()

        if not resume_text.strip():
            st.error("⚠️ Couldn’t extract any text from the PDF. Try a different file.")
            st.stop()

        st.success("✅ Resume extracted successfully!")

        st.subheader("📄 Resume Preview")
        st.text(resume_text[:1000])  # Limit preview

        st.subheader("📝 Job Description Preview")
        st.text(job_desc[:1000])

        with st.spinner("🧠 Analyzing with GPT..."):
            prompt = f"""
            You are an AI career assistant.

            Given this resume:
            {resume_text}

            And this job description:
            {job_desc}

            Compare them and return:
            - ✅ Skills that match
            - ❌ Skills that are missing
            - 💡 Suggestions to improve the resume

            Format clearly using bullet points and headings.
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )

                feedback = response.choices[0].message.content
                st.subheader("📊 AI Resume Feedback")
                st.markdown(feedback)

                # Save as .txt
                with open("feedback.txt", "w", encoding="utf-8") as f:
                    f.write(feedback)

                with open("feedback.txt", "rb") as f:
                    st.download_button(
                        label="📥 Download Feedback",
                        data=f,
                        file_name="resume_feedback.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"❌ GPT error: {e}")
    else:
        st.warning("⚠️ Please upload a resume and paste a job description.")
