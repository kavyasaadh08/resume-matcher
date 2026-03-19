import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="Bulk Resume Matcher", layout="centered")

st.title("📄 Bulk Resume vs JD Matcher")

# Upload multiple resumes
uploaded_files = st.file_uploader(
    "Upload Multiple Resumes (PDF)", 
    type=["pdf"], 
    accept_multiple_files=True
)

# Paste Job Description
jd_text = st.text_area("Paste Job Description here")

def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

if uploaded_files and jd_text:

    jd_words = set(jd_text.lower().split())

    results = []

    for file in uploaded_files:
        resume_text = extract_text(file)
        resume_words = set(resume_text.lower().split())

        matched = resume_words.intersection(jd_words)
        match_percent = (len(matched) / len(jd_words)) * 100 if jd_words else 0

        results.append({
            "name": file.name,
            "match": round(match_percent, 2),
            "matched_words": list(matched)[:20]
        })

    # Sort by best match
    results = sorted(results, key=lambda x: x["match"], reverse=True)

    st.subheader("📊 Ranking of Candidates")

    for res in results:
        st.write(f"**{res['name']}** → {res['match']} % match")
        st.write(f"Matched Keywords: {res['matched_words']}")
        st.markdown("---")