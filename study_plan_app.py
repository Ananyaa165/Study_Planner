import streamlit as st
from datetime import date, timedelta
import pandas as pd

st.set_page_config(page_title="AI Study Planner", layout="wide")

# ---- CUSTOM CSS ----
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stTitle {
        color: #2c3e50;
        text-align: center;
        font-weight: 600;
    }
    .stSubheader {
        color: #34495e;
        border-bottom: 2px solid #3498db;
        padding-bottom: 5px;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stExpander {
        border-radius: 5px;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("### 📖 Study Tips")
    with st.expander("💡 Helpful Tips for Effective Studying"):
        st.markdown("""
        - **Consistency is key**: Study a little every day rather than cramming.
        - **Active recall**: Test yourself on the material instead of just re-reading.
        - **Focus on weak areas**: Spend more time on subjects you find challenging.
        - **Take breaks**: Use techniques like Pomodoro (25 minutes study, 5 minutes break).
        - **Stay healthy**: Get enough sleep, eat well, and exercise regularly.
        """)

st.title("📚 Adaptive Study Planner")
st.markdown("#### Generate a smart study plan based on your strengths and exam date.")
st.markdown("---")

# ---- INPUTS ----
col1, col2 = st.columns(2)

with col1:
    subjects_input = st.text_input("📚 Enter subjects (comma separated)", placeholder="e.g., Math, Physics, Chemistry")
    weak_subjects = st.text_input("⚠️ Weak subjects (comma separated)", placeholder="e.g., Physics")
    strong_subjects = st.text_input("✅ Strong subjects (comma separated)", placeholder="e.g., Math")

with col2:
    study_hours = st.slider("⏰ Study hours per day", 1, 10, 4, help="Recommended: 4-6 hours")
    exam_date = st.date_input("📅 Exam date", min_value=date.today())

st.markdown("---")
generate_button = st.button("🚀 Generate Plan", use_container_width=True)

if generate_button and subjects_input:
    subjects = [s.strip() for s in subjects_input.split(",")]
    today = date.today()
    days_left = (exam_date - today).days

    if days_left <= 0:
        st.error("Exam date must be in the future")
        st.stop()

    st.subheader("📊 Summary")
    st.write(f"Days remaining: **{days_left}**")
    st.write(f"Total available study hours: **{days_left * study_hours} hrs**")

    # ---- PRIORITY WEIGHTS ----
    weak_list = [w.strip().lower() for w in weak_subjects.split(",") if w]
    strong_list = [s.strip().lower() for s in strong_subjects.split(",") if s]

    def get_weight(sub):
        if sub.lower() in weak_list:
            return 3
        elif sub.lower() in strong_list:
            return 1
        else:
            return 2

    weights = {sub: get_weight(sub) for sub in subjects}
    total_weight = sum(weights.values())

    st.subheader("📈 Priority Analysis")
    for sub, w in weights.items():
        level = "Hard" if w == 3 else "Easy" if w == 1 else "Medium"
        st.write(f"**{sub}** → {level}")

    # ---- PLAN GENERATION ----
    plan = []
    revision_start = int(days_left * 0.75)

    for day in range(days_left):
        current_date = today + timedelta(days=day)

        if day >= revision_start:
            task_type = "Revision"
        else:
            task_type = "Learning/Practice"

        # choose subject based on weight rotation
        # rotate subjects but bias toward higher weight
        weighted_list = []
        for s,w in weights.items():
            weighted_list.extend([s]*w)
        subject_choice = weighted_list[day % len(weighted_list)]

        plan.append({
            "Date": current_date,
            "Subject": subject_choice,
            "Task": task_type,
            "Hours": round(study_hours * (weights[subject_choice] / total_weight), 2)
        })

    df = pd.DataFrame(plan)

    st.subheader("🗓️ Generated Study Plan")
    st.dataframe(df, use_container_width=True)

    st.success("Plan generated successfully! Good luck for your exams 🍀")
