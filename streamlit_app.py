import streamlit as st
import requests
import json

# 🔐 간단한 패스워드 보호
PASSWORD = st.secrets["PASSKEY"]

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 Access Protected")
    password = st.text_input("Enter password", type="password")
    if st.button("Submit"):
        if password == PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ Incorrect password")
    st.stop()

# ✅ API 키 설정
API_KEY = st.secrets["OPENAI_API_KEY"]
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def generate_prompt(task):
    """Generates a focused prompt for Avionics software tasks."""
    if task == "Requirement":
        st.subheader("Define the Software Requirement")
        feature_name = st.text_input("Feature Name (e.g., Flight Data Logging, Autopilot Mode Indication):")
        user_story = st.text_area("User Story (As a [user role], I want [goal] so that [benefit]):")
        acceptance_criteria = st.text_area("Acceptance Criteria (Specific, measurable conditions of satisfaction):")
        technical_constraints = st.text_area("Technical Constraints (e.g., DO-178C Level, Interface Specifications):")

        if feature_name and user_story and acceptance_criteria:
            final_prompt = f"""
            Please create a new software requirement document for Jira system via given info {feature_name}, {user_story}, {acceptance_criteria}, {technical_constraints}
            """
        else:
            final_prompt = ""

    elif task == "Email/Chat":
        st.subheader("Compose Professional Communication")
        recipient = st.text_input("Recipient (e.g., Engineering Team, Certification Authority):")
        subject = st.text_input("Subject:")
        key_points = st.text_area("Key Points to Convey (Clearly and concisely):")
        urgency = st.selectbox("Urgency Level:", ["Normal", "High", "Informational"])

        if recipient and subject and key_points:
            final_prompt = f"""
            **Compose a communication (Email/Chat) to:** {recipient}

            **Subject:** {subject}

            **Key Points:**
            {key_points}

            **Urgency:** {urgency}

            Please draft a professional and clear message addressing the above points, suitable for the Avionics industry context.
            """
        else:
            final_prompt = ""

    elif task == "Monthly Accomplish":
        st.subheader("Summarize Monthly Progress")
        month = st.selectbox("Select Month:", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        key_achievements = st.text_area("Key Achievements This Month (Focus on deliverables and progress):")
        challenges_faced = st.text_area("Key Challenges and Mitigation Strategies:")
        next_steps = st.text_area("Planned Next Steps for the Following Month:")

        if month and key_achievements:
            final_prompt = f"""
            **Monthly Progress Summary for:** {month}

            **Key Achievements:**
            {key_achievements}

            **Challenges Faced and Mitigation Strategies:**
            {challenges_faced}

            **Planned Next Steps:**
            {next_steps}

            Provide a concise and professional summary of the monthly progress based on the above information, suitable for stakeholder reporting in an Avionics software project.
            """
        else:
            final_prompt = ""

    elif task == "Research":
        st.subheader("Conduct Targeted Research")
        research_area = st.text_input("Specific Research Area (e.g., RTOS Comparison, Cybersecurity Standards):")
        key_questions = st.text_area("Key Questions to Answer (Focus and actionable):")
        desired_format = st.selectbox("Desired Output Format:", ["Summary Report", "List of Findings", "Comparative Analysis"])

        if research_area and key_questions:
            final_prompt = f"""
            **Research Topic:** {research_area}

            **Key Questions to Answer:**
            {key_questions}

            **Desired Output Format:** {desired_format}

            Conduct focused research on the above topic and provide the findings in the format of a '{desired_format}'. Ensure the information is relevant to the Avionics industry and adheres to professional standards.
            """
        else:
            final_prompt = ""

    else:
        final_prompt = ""

    return final_prompt


# UI
st.title("🧑‍💼 Professional TPO♥")
st.subheader("As a Technical Product Owner, provide the necessary inputs below.")

task = st.selectbox("Choose Task", ["Requirement", "Email/Chat", "Monthly Accomplish", "Research"])

final_prompt = generate_prompt(task)

if final_prompt:
    st.subheader("Generated Prompt for Your Task:")
    st.text_area("Prompt to use:", value=final_prompt, height=400)

if st.button("Start New Task"):
    st.rerun()