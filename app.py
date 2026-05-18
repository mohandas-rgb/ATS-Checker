import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="ATA Checker", page_icon="📋", layout="centered")

st.title("📋 ATA Checker (ATS Screening Tool)")
st.write("Paste the Job Description and Candidate Resume below to analyze the match.")

# 2. Sidebar for API Key (Keep it secure!)
st.sidebar.header("Setup")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
st.sidebar.markdown("[Get a free Gemini API Key here](https://aistudio.google.com/)")

# 3. User Inputs
jd_text = st.text_area("Job Description (JD)", height=200, placeholder="Paste the job description here...")
resume_text = st.text_area("Candidate Resume", height=250, placeholder="Paste the resume text here...")

# 4. The Master Prompt Template
SYSTEM_PROMPT = """
Act as an expert Corporate Recruiter and ATS (Applicant Tracking System) Specialist. Your name is "ATA Checker." 
Your task is to analyze the provided Job Description (JD) against the Resume and provide a highly objective, accurate gap analysis.

Please provide the analysis using the following structured format:
1. **Match Score:** A percentage rating (0-100%) based on the alignment.
2. **Key Requirements Met:** Bullet points of specific hard skills, tools, and years of experience matched.
3. **Gaps / Missing Skills:** Bullet points of critical requirements missing.
4. **Keyword Optimization:** Words from the JD missed by the candidate.
5. **Final Recommendation:** [Strong Shortlist / Potential Match / Proceed with Caution / Reject] with a 2-sentence justification.
"""

# 5. Run Analysis
if st.button("Analyze Application"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not jd_text or not resume_text:
        st.warning("Please fill in both the Job Description and the Resume fields.")
    else:
        with st.spinner("ATA Checker is analyzing the resume against the JD..."):
            try:
                # Configure Gemini
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Combine prompt and data
                full_prompt = f"{SYSTEM_PROMPT}\n\n### Job Description:\n{jd_text}\n\n### Candidate Resume:\n{resume_text}"
                
                # Generate Response
                response = model.generate_content(full_prompt)
                
                # Display Results
                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
