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

st.title("Professional TPO")

task = st.selectbox(
    "Choose Task",
    ["Requirement Improvement", "Email/Chat Revision", "Monthly Accomplishment Refinement", "Research"],
)

final_prompt = generate_prompt(task)

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
        else:
            st.error(f"Error {response.status_code}: {response.text}")