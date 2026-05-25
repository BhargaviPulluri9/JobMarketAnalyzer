from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    import streamlit as st
    api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

def extract_skills(job_description):
    prompt = skill_extraction_prompt(job_description)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return parse_sections(response.text)

def analyze_gap(job_description, resume_text):
    prompt = gap_analysis_prompt(job_description, resume_text)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return parse_sections(response.text)

def parse_sections(text):
    sections = {}
    current_key = None
    current_items = []

    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.endswith(':') and line.isupper():
            if current_key:
                sections[current_key] = current_items
            current_key = line[:-1]
            current_items = []
        elif line.startswith('- '):
            current_items.append(line[2:])
        elif line[0].isdigit() and '. ' in line:
            current_items.append(line.split('. ', 1)[1])
        else:
            current_items.append(line)

    if current_key:
        sections[current_key] = current_items

    return sections