import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import io

# 1. Page Configuration
st.set_page_config(page_title="ATA Checker Pro", page_icon="📋", layout="wide")

st.title("📋 ATA Checker Pro (Multi-Resume Screening)")
st.write("Upload a Job Description and multiple resumes to scan them all at once.")

# 2. Sidebar for API Key
st.sidebar.header("Setup")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
st.sidebar.markdown("[Get a free Gemini API Key here](https://aistudio.google.com/)")

# Helper function to extract text from PDF or TXT
def extract_text(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    else:
        return uploaded_file.read().decode("utf-8")

# 3. User Inputs
jd_text = st.text_area("Job Description (JD)", height=150, placeholder="Paste the job description here...")
uploaded_resumes = st.file_uploader("Upload Resumes (PDF or TXT)", type=["pdf", "txt"], accept_multiple_files=True)

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
if st.button("Analyze All Resumes"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not jd_text or not uploaded_resumes:
        st.warning("Please fill in the Job Description and upload at least one resume.")
    else:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        st.success(f"Processing {len(uploaded_resumes)} resume(s)...")
        
        # Loop through each resume
        for index, file in enumerate(uploaded_resumes):
            with st.spinner(f"Analyzing {file.name}..."):
                try:
                    # Extract the text from the file
                    resume_text = extract_text(file)
                    
                    if not resume_text.strip():
                        st.error(f"Could not extract text from {file.name}. It might be empty or a scanned image.")
                        continue
                    
                    # Combine prompt and data
                    full_prompt = f"{SYSTEM_PROMPT}\n\n### Job Description:\n{jd_text}\n\n### Candidate Resume:\n{resume_text}"
                    
                    # Generate Response
                    response = model.generate_content(full_prompt)
                    
                    # Display Results inside an organized expander block
                    with st.expander(f"📄 Results for: {file.name}", expanded=True):
                        st.markdown(response.text)
                        
                except Exception as e:
                    st.error(f"An error occurred while processing {file.name}: {e}")
                    
        st.balloons() # Fun celebration when all processing is done!
