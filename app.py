import streamlit as st
import random
import json
import hashlib
from datetime import datetime, date

st.set_page_config(page_title="EconoLearn", page_icon="🎨", layout="wide")

# ─────────────────────────────────────────────
# CSS OVERHAUL (FIXING WHITE SQUARES & HOVER)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');

    /* Global Text & Background */
    html, body, [class*="st-emotion-cache"], .stApp {
        font-family: 'Nunito', sans-serif;
        background-color: #fffaf0 !important;
        color: #432818 !important; 
    }

    [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] h1, 
    [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] li, [data-testid="stMarkdownContainer"] span {
        color: #432818 !important;
    }

    .main-title { 
        font-size: 3.5rem; font-weight: 800; color: #ff85a2 !important; 
        text-shadow: 2px 2px 0px #ffe5ec; text-align: center; margin-bottom: 0px;
    }
    
    .subtitle { 
        color: #6d6875 !important; font-size: 1.3rem; text-align: center;
        font-weight: 700; margin-bottom: 2rem;
    }

    /* Comic Style Cards */
    .card { 
        background: #ffffff !important; border-radius: 30px; padding: 1.5rem; 
        margin-bottom: 1.5rem; border: 4px solid #f1f2f6; box-shadow: 8px 8px 0px #e0e0e0;
    }
    
    .card-blue { border-color: #bae6fd !important; background: #f0f9ff !important; box-shadow: 8px 8px 0px #bae6fd; }
    .card-green { border-color: #bbf7d0 !important; background: #f0fdf4 !important; box-shadow: 8px 8px 0px #bbf7d0; }
    .card-red { border-color: #fecaca !important; background: #fef2f2 !important; box-shadow: 8px 8px 0px #fecaca; }
    .card-gold { border-color: #fef08a !important; background: #fefce8 !important; box-shadow: 8px 8px 0px #fef08a; }

    /* 🎯 THE BUTTON FIX: Removing white squares and keyboard icons */
    .stButton > button {
        border-radius: 25px !important;
        border: none !important;
        background-color: #ffb7b2 !important; 
        padding: 0.6rem 1rem !important;
        box-shadow: 0px 5px 0px #ff8a8a !important;
        transition: all 0.1s ease !important;
        width: 100% !important;
        height: auto !important;
        min-height: 80px !important;
    }

    /* Force EVERYTHING inside the button to be transparent and bold */
    .stButton > button div, 
    .stButton > button p, 
    .stButton > button span,
    .stButton > button div[data-testid="stMarkdownContainer"] {
        background-color: transparent !important;
        background: transparent !important;
        color: #ffffff !important;
        font-weight: 800 !important; /* BOLD TEXT */
        font-size: 1.1rem !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Hide the "keyboard_double" and tooltip artifacts */
    .stButton > button small, .stButton > button svg {
        display: none !important;
        visibility: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(2px) !important;
        box-shadow: 0px 3px 0px #ff8a8a !important;
        background-color: #ff9aa2 !important;
        border: none !important;
    }

    /* Level Badge Stickers */
    .level-badge { 
        display: inline-block; padding: 6px 18px; border-radius: 20px; 
        font-size: 0.9rem; font-weight: 800; text-transform: uppercase; color: #ffffff !important;
    }
    .beginner { background: #0ea5e9 !important; }
    .intermediate { background: #f97316 !important; }
    .advanced { background: #84cc16 !important; }

    /* Sidebar Fixes */
    section[data-testid="stSidebar"] { background-color: #fff5f5 !important; border-right: 2px dashed #ffb7b2; }
    section[data-testid="stSidebar"] * { color: #432818 !important; }

    /* XP Bar */
    .xp-bar { background: #f1f2f6; border-radius: 50px; height: 22px; border: 3px solid #e2e8f0; overflow: hidden; }
    .xp-fill { background: linear-gradient(90deg, #ffb7b2, #ffdac1); height: 100%; border-radius: 50px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE & DATABASE
# ─────────────────────────────────────────────
if "xp" not in st.session_state: st.session_state.xp = 0
if "page" not in st.session_state: st.session_state.page = "Home"
if "topic" not in st.session_state: st.session_state.topic = "Supply & Demand"
if "level" not in st.session_state: st.session_state.level = "Beginner"

TOPICS = {
    "Supply & Demand": "🛒", "Inflation & Deflation": "💸", "GDP & Growth": "📊",
    "Monetary Policy": "🏦", "Fiscal Policy": "🏛️", "Labor Markets": "👷",
    "Trade & Globalization": "🌍", "Financial Markets": "📉", "Business Cycles": "🔄",
    "Behavioral Economics": "🧠",
}

LESSONS = {
    "Supply & Demand": {"Beginner": {"title": "The Basics", "content": "When people want something, prices go up!"}},
    "GDP & Growth": {"Beginner": {"title": "What is GDP?", "content": "GDP is the total value of all finished goods produced."}},
}

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🎨 EconoLearn</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"**Level {st.session_state.xp // 100} Explorer** ✨")
    st.markdown(f'<div class="xp-bar"><div class="xp-fill" style="width:{st.session_state.xp % 100}%"></div></div>', unsafe_allow_html=True)
    
    st.markdown("### 🗺️ Navigation")
    if st.button("🏠 Home"): st.session_state.page = "Home"
    if st.button("📚 Daily Lesson"): st.session_state.page = "Daily Lesson"
    if st.button("❓ Quiz"): st.session_state.page = "Quiz"
    
    st.markdown("---")
    st.markdown("### 🏆 Mastery Level")
    l_col1, l_col2 = st.columns(2)
    with l_col1:
        if st.button("Beginner"): st.session_state.level = "Beginner"
    with l_col2:
        if st.button("Advanced"): st.session_state.level = "Advanced"

# ─────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────
if st.session_state.page == "Home":
    st.markdown('<p class="main-title">🎨 EconoLearn</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Pick a topic and start your economic journey!</p>', unsafe_allow_html=True)

    st.markdown("### 🗺️ Explore All Topics")
    topic_cols = st.columns(5)
    
    # This loop generates the buttons you saw in your screenshot
    for i, (t, icon) in enumerate(TOPICS.items()):
        with topic_cols[i % 5]:
            # The label now includes the emoji and text in a bold format
            if st.button(f"{icon}\n{t}", key=f"btn_{t}"):
                st.session_state.topic = t
                st.session_state.page = "Daily Lesson"
                st.rerun()

elif st.session_state.page == "Daily Lesson":
    st.markdown(f"## {st.session_state.topic}")
    lesson = LESSONS.get(st.session_state.topic, LESSONS["Supply & Demand"]).get("Beginner")
    st.markdown(f"<div class='card card-blue'><b>{lesson['title']}</b><br><br>{lesson['content']}</div>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

elif st.session_state.page == "Quiz":
    st.markdown("## ❓ Quiz Time")
    st.markdown("<div class='card card-gold'>Quiz content coming soon!</div>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "Home"
        st.rerun()
