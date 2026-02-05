import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Translator!")
st.title("Translation Stand")
st.markdown(f"Translate between **English, Twi, French, Spanish, and Japanese**.")
api_key = os.getenv("api_key")

with st.sidebar:
    st.header("Settings")
    temp = st.slider("Creativity (Temperature)", 0.0, 2.0, 1.5, 0.1)
    st.info("Twi is a dialect spoken in Ghana. Gemini handles it surprisingly well!")

# Translation Flow
def translate_text(user_input, temperature, key):
    try:
        client = genai.Client(api_key=key)
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            config=types.GenerateContentConfig(
                system_instruction=f"""You are a system that translates English to Twi and Twi to English, French, Spanish, and Japanese. 
                Provide direct translations without extra conversational filler.
                Present the result in this structure
                    - English
                    - Twi
                    - French
                    - Spanish
                    - Japanesse""",
                temperature=temperature
            ),
            contents=user_input
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

prompt = st.text_area("Enter text to translate:", placeholder="e.g., Wo ho te s3n?")

if st.button("Translate"):
    if not api_key:
        st.error("Please enter your API key first!")
    elif not prompt:
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            result = translate_text(prompt, temp, api_key)
            st.subheader("Result:")
            st.success(result)
