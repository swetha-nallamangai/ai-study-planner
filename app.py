
import streamlit as st
from datetime import date
from planner import generate_plan

st.set_page_config(page_title="AI Study Planner", page_icon="📚")

st.title("📚 AI Study Planner")
st.write("Create a personalized study timetable.")

subjects_input = st.text_input(
    "Enter subjects separated by commas",
    "Python, DBMS, Mathematics"
)

hours = st.number_input(
    "Study hours per day",
    min_value=1,
    max_value=12,
    value=3
)

days = st.number_input(
    "Number of study days",
    min_value=1,
    max_value=60,
    value=7
)

subjects = list(dict.fromkeys(
    s.strip() for s in subjects_input.split(",") if s.strip()
))

difficulties = {}

if subjects:
    st.subheader("Choose subject difficulty")
    for subject in subjects:
        difficulties[subject] = st.selectbox(
            f"{subject} difficulty",
            ["Easy", "Medium", "Hard"],
            index=1
        )



if "plan" not in st.session_state:
    st.session_state.plan = []

if st.button("Generate My Study Plan", type="primary"):
    if not subjects:
        st.error("Please enter at least one subject.")
    else:
        st.session_state.plan = generate_plan(
            subjects, difficulties, hours, days
        )
        st.success("Your study plan has been generated!")

if st.session_state.plan:
    st.subheader("Your Study Timetable")

    plan = st.session_state.plan

    for day in sorted(set(item["Day"] for item in plan)):
        with st.expander(f"Day {day}", expanded=(day == 1)):
            for index, item in enumerate(plan):
                if item["Day"] == day:
                    label = (
                        f'{item["Subject"]} - '
                        f'{item["Minutes"]} minutes '
                        f'({item["Difficulty"]})'
                    )
                    item["Completed"] = st.checkbox(
                        label,
                        value=item["Completed"],
                        key=f"task_{index}"
                    )

    completed = sum(item["Completed"] for item in plan)
    progress = completed / len(plan)

    st.subheader("Study Progress")
    st.progress(progress)
    st.write(f"{completed} of {len(plan)} sessions completed")

    st.subheader("Download Your Plan")
    import csv
    import io

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["Day", "Subject", "Difficulty",
                    "Minutes", "Completed"]
    )
    writer.writeheader()
    writer.writerows(plan)

    st.download_button(
        "Download CSV",
        data=output.getvalue(),
        file_name="study_plan.csv",
        mime="text/csv"
    )
