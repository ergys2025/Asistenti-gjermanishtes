import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI

st.set_page_config(page_title="Asistenti i Gjermanishtes")
st.title("Asistenti i Gjermanishtes")
st.write("Ngarko një libër PDF në gjermanisht dhe bëj pyetje në shqip.")

pdf = st.file_uploader("Ngarko librin (PDF)", type=["pdf"])

if pdf:
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    question = st.text_input("Shkruaj pyetjen që ke për librin")

    if question:
        with st.spinner("Po kërkoj përgjigjen..."):

            client = OpenAI(api_key=st.secrets["openai"]["api_key"])

            prompt = f"""
Ti je një mësues i gjermanishtes. Përdor vetëm tekstin më poshtë për të dhënë një përgjigje të saktë dhe të kuptueshme në shqip për pyetjen.

TEKSTI:
{text}

PYETJA:
{question}

PËRGJIGJJA NË SHQIP:
"""

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            answer = response.choices[0].message.content
            st.success("Përgjigjja:")
            st.write(answer)
