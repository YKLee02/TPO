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

# UI
st.title("🧑‍💼 Professional Rewriter for Eunice♥")

tone = st.selectbox("Choose tone", ["Friendly", "Formal", "Polite", "Confident"])
text_input = st.text_area("Enter your sentence in English")

if st.button("Rewrite"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        prompt = (
            f"You are a friendly and professional plastic surgery coordinator who frequently communicates with patients via text or email.\n"
            f"Rewrite the following sentence in a {tone.lower()} tone to sound more empathetic, warm, and informative while maintaining professionalism:\n\n"
            f"\"{text_input}\""
            )

        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
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