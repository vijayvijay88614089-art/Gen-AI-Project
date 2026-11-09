from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

from modules.database import initialize

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")
st.set_page_config(page_title="InsightForge AI", page_icon="🔎", layout="wide", initial_sidebar_state="expanded")
initialize()
css = ROOT / "assets" / "styles.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

NAV = [
    ("pages/01_Home.py", "Home Dashboard", "🏠"),
    ("pages/02_AI_Fundamentals.py", "AI Fundamentals", "🧭"),
    ("pages/03_Generative_Models.py", "Generative Models", "🧬"),
    ("pages/04_Deep_Learning.py", "Deep Learning Models", "🧠"),
    ("pages/05_Transformers_LLMs.py", "Transformers and LLMs", "🔤"),
    ("pages/06_Prompt_Engineering.py", "Prompt Engineering Playground", "✍️"),
    ("pages/07_Data_Analyst.py", "AI Data Analyst", "📊"),
    ("pages/08_RAG_Assistant.py", "RAG Document Assistant", "📚"),
    ("pages/09_AI_Agent.py", "AI Agent", "🛠️"),
    ("pages/10_Multimodal_AI.py", "Multimodal AI", "🎙️"),
    ("pages/11_Responsible_AI.py", "Responsible AI", "🛡️"),
    ("pages/12_Industry_Applications.py", "Industry Applications", "🏭"),
    ("pages/13_Evaluation.py", "Project Evaluation", "📈"),
    ("pages/14_About.py", "About Project", "ℹ️"),
]
pages = [st.Page(str(ROOT / file), title=title, icon=icon, default=(i == 0)) for i, (file, title, icon) in enumerate(NAV)]
st.navigation(pages, position="sidebar").run()
