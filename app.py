import streamlit as st
import openai
import pdfplumber

st.set_page_config(page_title="Resume Analyzer", page_icon="🧠")
st.title("🧠 AI-Powered Resume Analyzer")

st.write("Upload your resume and a job description. Get GPT feedback on how well your resume matches!")

# 🗝️ Ask for OpenAI API key
user_api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")

if not user_api_key:
    st.warning("⚠️ Please enter your OpenAI API key to continue.")
    st.stop()

# Create OpenAI client
client = openai.OpenAI(api_key=user_api_key)

# Upload resume
resume_file = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])

# Paste job description
job_desc = st.text_area("📝 Paste the Job Description here")

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Analyze Button
if st.button("Analyze"):
    if resume_file and job_desc.strip():
        st.info("⏳ Extracting text from resume...")
        try:
            resume_text = extract_text_from_pdf(resume_file)
        except Exception as e:
            st.error(f"❌ Error reading the resume: {e}")
            st.stop()

        if not resume_text.strip():
            st.error("⚠️ No text found in resume. Try a different file.")
            st.stop()

        st.success("✅ Resume text extracted!")
        st.subheader("📄 Resume Preview")
        st.text(resume_text[:1000])  # Show first 1000 chars

        st.subheader("📝 Job Description Preview")
        st.text(job_desc[:1000])

        # Build the prompt
        prompt = f"""
        You are an AI career assistant.

        Given the following resume:
        {resume_text}

        And the following job description:
        {job_desc}

        Provide:
        - ✅ Skills that match
        - ❌ Skills missing
        - 💡 Suggestions to improve the resume

        Format your response using clear headings and bullet points.
        """

        # AI Analysis
        with st.spinner("🧠 Analyzing with GPT..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )

                feedback = response.choices[0].message.content
                st.subheader("📊 AI Resume Feedback")
                st.markdown(feedback)

                # Save feedback to text file
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
                st.error(f"❌ OpenAI API Error: {e}")
    else:
        st.warning("⚠️ Please upload a resume and paste a job description.")
