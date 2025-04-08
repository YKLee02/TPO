import streamlit as st
import requests
import json

# 🔐 간단한 패스워드 보호
PASSWORD = st.secrets["PASSKEY"]

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 Access Protected")

    # ✨ Use form to allow Enter key to submit
    with st.form("password_form"):
        password = st.text_input("Enter password", type="password")
        submitted = st.form_submit_button("Submit")  # Form's submit button

        if submitted:
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
    """Generates a prompt for AI-driven improvement/revision of documents based on the task."""
    if task == "Requirement Improvement":
        original_requirement = st.text_area("Original Requirement Text:", height=200)
        final_prompt = f"""
        Please correct and improve this original software requirement document: {original_requirement}. 
        The output should be the title of the requirement, User story, and Acceptance Criteria (Table style) including non-function acceptance criteria.
        """
        return final_prompt

    elif task == "Email/Chat Revision":
        original_requirement = st.text_area("Original Requirement Text:", height=200)
        final_prompt = f"""
        Please correct and improve this original email or chat contents: {original_requirement}. 
        """
        return final_prompt

    elif task == "Monthly Accomplishment Refinement":
        original_requirement = st.text_area("Original Requirement Text:", height=200)
        final_prompt = f"""
        Please correct and improve this original contents with bulletin points: {original_requirement}. 
        """
        return final_prompt

    elif task == "Research":
        original_requirement = st.text_area("Original Requirement Text:", height=200)
        final_prompt = f"""
        Please provide basic background knowledge about this: {original_requirement}. And please provide a link for good references.
        """
        return final_prompt

    return None

st.title("Professional TPO!!")

task = st.selectbox(
    "Choose Task",
    ["Requirement Improvement", "Email/Chat Revision", "Monthly Accomplishment Refinement", "Research"],
)

final_prompt = generate_prompt(task)

# 🆕 Initialize session state to store previous AI answer
if "previous_answer" not in st.session_state:
    st.session_state["previous_answer"] = ""

if final_prompt:
    if st.button("Rewrite"):
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [{"text": final_prompt}]
                }
            ]
        }

        response = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            result = response.json()
            rewritten = result["candidates"][0]["content"]["parts"][0]["text"]
            st.success(rewritten)

            # 🆕 Save the rewritten text
            st.session_state["previous_answer"] = rewritten
        else:
            st.error(f"Error {response.status_code}: {response.text}")

# 🆕 Feedback section to revise previous AI output
if st.session_state["previous_answer"]:
    st.subheader("🔄 Revise Previous Answer with Feedback")
    feedback = st.text_area("Enter your feedback to improve the previous answer", key="feedback_input", height=100)
    
    if st.button("Revise with Feedback"):
        if feedback.strip() == "":
            st.warning("⚠️ Please enter your feedback before revising.")
        else:
            revised_prompt = f"""
            Here is the previous AI answer: "{st.session_state['previous_answer']}".
            Please revise it based on this user feedback: "{feedback}".
            """

            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "parts": [{"text": revised_prompt}]
                    }
                ]
            }

            response = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                result = response.json()
                revised_text = result["candidates"][0]["content"]["parts"][0]["text"]
                st.success(revised_text)
                
                # 🆕 Update previous_answer with new revision
                st.session_state["previous_answer"] = revised_text
            else:
                st.error(f"Error {response.status_code}: {response.text}")