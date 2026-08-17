import streamlit as st

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="🎓",
    layout="wide"
)

# ---------------- TITLE ----------------

st.title("🎓 Student Performance Analysis")
st.write(
    "Analyze academic performance and get personalized improvement suggestions."
)

st.divider()

# ---------------- STUDENT DETAILS ----------------

st.header("👨‍🎓 Student Details")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Student Name")

with col2:
    student_id = st.text_input("Student ID")

st.divider()

# ---------------- ACADEMIC DETAILS ----------------

st.header("📚 Academic Details")

col1, col2 = st.columns(2)

with col1:
    study_hours = st.number_input(
        "Study Hours per Day",
        min_value=0.0,
        max_value=24.0,
        value=2.0,
        step=0.5
    )

with col2:
    attendance = st.number_input(
        "Attendance (%)",
        min_value=0.0,
        max_value=100.0,
        value=75.0,
        step=1.0
    )

col1, col2, col3 = st.columns(3)

with col1:
    assignment_marks = st.number_input(
        "Assignment Marks (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0,
        step=1.0
    )

with col2:
    internal_marks = st.number_input(
        "Internal Marks (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0,
        step=1.0
    )

with col3:
    exam_marks = st.number_input(
        "Exam Marks (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0,
        step=1.0
    )

st.divider()

# ---------------- SUBJECT SELECTION ----------------

st.header("📖 Select Your Subjects")

all_subjects = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Science",
    "English",
    "Tamil",
    "Hindi",
    "Accountancy",
    "Commerce",
    "Economics",
    "History",
    "Geography"
]

selected_subjects = st.multiselect(
    "Choose the subjects you are studying:",
    all_subjects,
    default=[
        "Mathematics",
        "English",
        "Computer Science"
    ]
)

# ---------------- SUBJECT MARKS ----------------

subject_marks = {}

if selected_subjects:

    st.subheader("📝 Enter Subject Marks")

    columns = st.columns(3)

    for i, subject in enumerate(selected_subjects):

        with columns[i % 3]:

            subject_marks[subject] = st.number_input(
                f"{subject} Marks (%)",
                min_value=0.0,
                max_value=100.0,
                value=70.0,
                step=1.0,
                key=f"mark_{subject}"
            )

else:

    st.info("Please select at least one subject.")

st.divider()

# ---------------- ANALYZE BUTTON ----------------

if st.button(
    "📊 Analyze My Performance",
    use_container_width=True
):

    if name.strip() == "":
        st.warning("⚠️ Please enter your name.")

    elif student_id.strip() == "":
        st.warning("⚠️ Please enter your Student ID.")

    elif len(selected_subjects) == 0:
        st.warning("⚠️ Please select at least one subject.")

    else:
        st.session_state["analyzed"] = True


# =========================================================
# RESULTS
# =========================================================

if st.session_state.get("analyzed", False):

    # ---------------- OVERALL CALCULATION ----------------

    average_marks = (
        assignment_marks +
        internal_marks +
        exam_marks
    ) / 3

    study_score = min(study_hours * 10, 100)

    performance_score = (
        average_marks * 0.7 +
        attendance * 0.2 +
        study_score * 0.1
    )

    # ---------------- GRADE ----------------

    if average_marks >= 90:
        grade = "A+"
    elif average_marks >= 80:
        grade = "A"
    elif average_marks >= 70:
        grade = "B"
    elif average_marks >= 60:
        grade = "C"
    elif average_marks >= 50:
        grade = "D"
    else:
        grade = "F"

    # ---------------- PASS / FAIL ----------------

    if average_marks >= 50:
        result = "PASS ✅"
    else:
        result = "FAIL ❌"

    # ---------------- PERFORMANCE LEVEL ----------------

    if performance_score >= 85:
        level = "Excellent 🌟"
    elif performance_score >= 70:
        level = "Good 👍"
    elif performance_score >= 50:
        level = "Average 🙂"
    else:
        level = "Needs Improvement 📚"

    # ---------------- DASHBOARD ----------------

    st.success(f"✅ Analysis completed for {name}!")

    st.header("📊 Performance Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Average Marks",
            f"{average_marks:.1f}%"
        )

    with col2:
        st.metric(
            "Performance Score",
            f"{performance_score:.1f}%"
        )

    with col3:
        st.metric(
            "Grade",
            grade
        )

    with col4:
        st.metric(
            "Result",
            result
        )

    st.divider()

    # ---------------- PERFORMANCE LEVEL ----------------

    st.subheader("🏆 Performance Level")

    if performance_score >= 85:
        st.success(level)
    elif performance_score >= 70:
        st.info(level)
    elif performance_score >= 50:
        st.warning(level)
    else:
        st.error(level)

    st.write("Overall Performance")

    st.progress(
        min(int(performance_score), 100)
    )

    st.divider()

    # ---------------- SUBJECT ANALYSIS ----------------

    st.subheader("📚 Subject-wise Performance")

    # Subject chart

    st.bar_chart(subject_marks)

    highest_mark = max(subject_marks.values())
    lowest_mark = min(subject_marks.values())

    # Check equal marks

    if highest_mark == lowest_mark:

        st.info(
            "⚖️ All selected subjects have the same marks."
        )

        strongest_subject = "All subjects"
        weakest_subject = "All subjects"

    else:

        strongest_subject = max(
            subject_marks,
            key=subject_marks.get
        )

        weakest_subject = min(
            subject_marks,
            key=subject_marks.get
        )

        col1, col2 = st.columns(2)

        with col1:
            st.success(
                f"🏆 Strongest Subject: "
                f"{strongest_subject} "
                f"({subject_marks[strongest_subject]:.0f}%)"
            )

        with col2:
            st.warning(
                f"📌 Subject to Improve: "
                f"{weakest_subject} "
                f"({subject_marks[weakest_subject]:.0f}%)"
            )

    st.divider()

    # ---------------- SUBJECT AVERAGE ----------------

    subject_average = sum(
        subject_marks.values()
    ) / len(subject_marks)

    st.subheader("📈 Subject Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Subjects Selected",
            len(selected_subjects)
        )

    with col2:
        st.metric(
            "Subject Average",
            f"{subject_average:.1f}%"
        )

    with col3:
        st.metric(
            "Highest Mark",
            f"{highest_mark:.0f}%"
        )

    st.divider()

    # ---------------- WEAK AREA DETECTION ----------------

    st.subheader("🎯 Weak Area Detection")

    areas = {
        "Attendance": attendance,
        "Assignment": assignment_marks,
        "Internal": internal_marks,
        "Exam": exam_marks
    }

    weakest_area = min(
        areas,
        key=areas.get
    )

    weakest_value = areas[weakest_area]

    st.info(
        f"📌 Your main academic area to improve is "
        f"**{weakest_area}** with a score of "
        f"**{weakest_value:.0f}%**."
    )

    # ---------------- SUBJECT WARNING ----------------

    if lowest_mark < 60:

        st.warning(
            f"📚 Your lowest subject mark is "
            f"{lowest_mark:.0f}%. "
            f"Give additional attention to this subject."
        )

    st.divider()

    # ---------------- SMART RECOMMENDATIONS ----------------

    st.subheader("💡 Smart Recommendations")

    suggestions = []

    if study_hours < 3:

        suggestions.append(
            "📚 Increase your daily study time gradually."
        )

    if attendance < 75:

        suggestions.append(
            "🏫 Try to improve your class attendance."
        )

    if assignment_marks < 60:

        suggestions.append(
            "📝 Spend more time completing assignments."
        )

    if internal_marks < 60:

        suggestions.append(
            "📖 Focus more on internal assessments."
        )

    if exam_marks < 60:

        suggestions.append(
            "✏️ Practice previous questions and revise regularly."
        )

    if lowest_mark < 60 and strongest_subject != "All subjects":

        suggestions.append(
            f"🎯 Give extra attention to {weakest_subject}."
        )

    if not suggestions:

        suggestions.append(
            "🌟 Great work! Keep maintaining your current performance."
        )

    for suggestion in suggestions:

        st.write(suggestion)

    st.divider()

    # =====================================================
    # WHAT-IF ANALYSIS
    # =====================================================

    st.subheader("🔮 What-If Analysis")

    st.write(
        "See how your performance score could change "
        "if you improve your weakest subject."
    )

    if strongest_subject == "All subjects":

        st.info(
            "All subjects currently have the same marks. "
            "Try changing one subject mark to use the What-If Analysis."
        )

    else:

        current_weakest_mark = int(
            subject_marks[weakest_subject]
        )

        improved_mark = st.slider(
            f"Improve {weakest_subject} mark",
            min_value=current_weakest_mark,
            max_value=100,
            value=current_weakest_mark,
            key="what_if_subject"
        )

        current_subject_average = (
            sum(subject_marks.values())
            / len(subject_marks)
        )

        future_subject_total = (
            sum(subject_marks.values())
            - subject_marks[weakest_subject]
            + improved_mark
        )

        future_subject_average = (
            future_subject_total
            / len(subject_marks)
        )

        # Future performance combines
        # overall marks + subject average

        future_score = (
            performance_score * 0.7
            + future_subject_average * 0.3
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Current Performance",
                f"{performance_score:.1f}%"
            )

        with col2:

            st.metric(
                "Possible Performance",
                f"{future_score:.1f}%",
                delta=f"{future_score - performance_score:.1f}%"
            )

        st.success(
            f"💡 If your {weakest_subject} mark improves "
            f"from {current_weakest_mark}% to {improved_mark}%, "
            f"your estimated performance score could become "
            f"{future_score:.1f}%."
        )

    st.divider()

    # ---------------- STUDENT SUMMARY ----------------

    st.subheader("📋 Student Summary")

    st.write(f"**Student Name:** {name}")

    st.write(f"**Student ID:** {student_id}")

    st.write(
        f"**Study Hours:** "
        f"{study_hours} hours/day"
    )

    st.write(
        f"**Attendance:** "
        f"{attendance}%"
    )

    st.write(
        f"**Average Marks:** "
        f"{average_marks:.1f}%"
    )

    st.write(
        f"**Subject Average:** "
        f"{subject_average:.1f}%"
    )

    st.write(
        f"**Grade:** "
        f"{grade}"
    )

    st.write(
        f"**Performance Level:** "
        f"{level}"
    )

    st.write(
        f"**Selected Subjects:** "
        f"{', '.join(selected_subjects)}"
    )

    st.divider()

    st.caption(
        "🎓 Student Performance Analysis | "
        "Data Science Project"
    )