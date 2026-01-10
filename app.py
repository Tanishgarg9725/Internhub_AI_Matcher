# 1. Imports
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# 2. Load env & configure Gemini
load_dotenv("API.env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-flash-lite-latest")

# 3. Helper functions ✅
def calculate_ats_score(student_skills, required_skills):
    matched = set(student_skills).intersection(set(required_skills))
    score = (len(matched) / len(required_skills)) * 100 if required_skills else 0
    return round(score, 2), list(matched)

def find_skill_gaps(student_skills, required_skills):
    return list(set(required_skills) - set(student_skills))

# # 4. Streamlit UI
# st.set_page_config(page_title="InternHub AI Matcher")
# st.title("🎯 InternHub – AI Internship Matcher")

# import streamlit as st

st.set_page_config(page_title="InternHub AI Matcher", layout="centered")

st.title("🎯 InternHub – AI Internship Matcher")
st.write("Simple AI tool to evaluate internship fit")

st.header("👨‍🎓 Student Profile")

student_skills = st.text_input(
    "Skills (comma-separated)", 
    "Python, Machine Learning, Pandas"
)

student_interests = st.text_input(
    "Interests (comma-separated)", 
    "AI, Data Science"
)

student_experience = st.text_area(
    "Experience",
    "Built ML projects and data analysis dashboards"
)
st.header("💼 Internship Description")

role = st.text_input("Role", "AI Intern")

required_skills = st.text_input(
    "Required Skills (comma-separated)",
    "Python, Machine Learning, Deep Learning, Docker"
)

jd_description = st.text_area(
    "Job Description",
    "Looking for an AI Intern to build and deploy ML models"
)
if st.button("🔍 Analyze Internship Match"):
    student_skills_list = [s.strip() for s in student_skills.split(",")]
    required_skills_list = [s.strip() for s in required_skills.split(",")]

    ats_score, matched_skills = calculate_ats_score(
        student_skills_list, required_skills_list
    )

    skill_gaps = find_skill_gaps(
        student_skills_list, required_skills_list
    )

    prompt = f"""
    You are an AI career assistant.

    Student Skills: {student_skills_list}
    Experience: {student_experience}

    Internship Role: {role}
    Required Skills: {required_skills_list}

    Tasks:
    1. Match summary
    2. Skill gap explanation
    3. Resume improvement tips
    4. Final recommendation
    """

    response = model.generate_content(prompt)
    ai_output = response.text
    st.subheader("📊 ATS Score")
    st.metric("Match Score", f"{ats_score}%")

    st.subheader("✅ Matched Skills")
    st.write(matched_skills)

    st.subheader("❌ Skill Gaps")
    st.write(skill_gaps)

    st.subheader("🤖 AI Analysis")
    st.markdown(ai_output)
