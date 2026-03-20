import streamlit as st
import random
import json
import hashlib
from datetime import datetime, date

st.set_page_config(page_title="EconoLearn", page_icon="🎨", layout="wide")

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "xp" not in st.session_state: st.session_state.xp = 0
if "page" not in st.session_state: st.session_state.page = "Home"
if "topic" not in st.session_state: st.session_state.topic = "Supply & Demand"
if "level" not in st.session_state: st.session_state.level = "Beginner"
if "streak" not in st.session_state: st.session_state.streak = 0

# ─────────────────────────────────────────────
# CSS OVERHAUL (NEW COLOR PALETTE)
# ─────────────────────────────────────────────
# Olivine: #A4BD84 | Straw: #D3DC92 | Vanilla: #FDF1A8 | Melon: #FCAB92 | Old Rose: #B17C82
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');

    /* Global App Background (Vanilla) */
    html, body, [class*="st-emotion-cache"], .stApp {
        font-family: 'Nunito', sans-serif;
        background-color: #FDF1A8 !important;
        color: #2D1B1E !important; /* Very dark Old Rose for text readability */
    }

    /* Sidebar Styling (Darker Olivine) */
    section[data-testid="stSidebar"] {
        background-color: #8da66d !important; /* Darkened Olivine */
        border-right: 3px solid #B17C82;
    }
    
    /* Ensure sidebar text is readable */
    section[data-testid="stSidebar"] * {
        color: #FDF1A8 !important; /* Vanilla text on green background */
    }

    /* Comic Style Cards (Straw background with Olivine border) */
    .card { 
        background: #D3DC92 !important; 
        border-radius: 30px; 
        padding: 1.5rem; 
        margin-bottom: 1.5rem; 
        border: 5px solid #A4BD84;
        box-shadow: 8px 8px 0px #B17C82; /* Old Rose Shadow */
    }
    
    .card b, .card span, .card h3 {
        color: #2D1B1E !important;
    }

    /* 🎯 BUTTONS (Melon background, Old Rose shadow) */
    .stButton > button {
        border-radius: 25px !important;
        border: none !important;
        background-color: #FCAB92 !important; /* Melon */
        padding: 0.6rem 1rem !important;
        box-shadow: 0px 6px 0px #B17C82 !important; /* Old Rose */
        transition: all 0.1s ease !important;
        width: 100% !important;
        min-height: 70px !important;
    }

    .stButton > button div, 
    .stButton > button p, 
    .stButton > button span {
        background-color: transparent !important;
        color: #2D1B1E !important; /* Dark text for contrast on Melon */
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }

    /* Hide Streamlit Button Artifacts */
    .stButton > button small, .stButton > button svg {
        display: none !important;
    }
    
    .stButton > button:hover {
        transform: translateY(2px) !important;
        box-shadow: 0px 3px 0px #B17C82 !important;
        background-color: #e8957d !important; /* Darkened Melon */
    }

    .main-title { 
        font-size: 3.5rem; font-weight: 800; color: #B17C82 !important; 
        text-shadow: 2px 2px 0px #A4BD84; text-align: center; margin-bottom: 10px;
    }
    
    .subtitle { 
        color: #8da66d !important; font-size: 1.3rem; text-align: center;
        font-weight: 700; margin-bottom: 2rem;
    }

    /* XP Bar */
    .xp-bar { background: #D3DC92; border-radius: 50px; height: 22px; border: 3px solid #A4BD84; overflow: hidden; }
    .xp-fill { background: #FCAB92; height: 100%; border-radius: 50px; }

    /* Level Badges */
    .level-badge { 
        display: inline-block; padding: 6px 18px; border-radius: 20px; 
        font-size: 0.9rem; font-weight: 800; color: #FDF1A8 !important;
    }
    .beginner { background: #A4BD84 !important; }
    .advanced { background: #B17C82 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────
TOPICS = {
    "Supply & Demand": "🛒", "Inflation & Deflation": "💸", "GDP & Growth": "📊",
    "Monetary Policy": "🏦", "Fiscal Policy": "🏛️", "Labor Markets": "👷",
    "Trade & Globalization": "🌍", "Financial Markets": "📉", "Business Cycles": "🔄",
    "Behavioral Economics": "🧠",
}

LESSONS = {
    "Supply & Demand": {"Beginner": {"title": "The Basics", "content": "When people want something, prices go up! This is the core of how markets move."}},
    "GDP & Growth": {"Beginner": {"title": "What is GDP?", "content": "GDP is the total value of all finished goods produced in a country."}},
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
    st.markdown("### 🏆 Mastery")
    if st.button("Beginner Level"): st.session_state.level = "Beginner"
    if st.button("Advanced Level"): st.session_state.level = "Advanced"

    st.markdown("---")
    st.caption("Tip: Use the arrow at the top to hide this sidebar!")

# ─────────────────────────────────────────────
# MAIN PAGES
# ─────────────────────────────────────────────
if st.session_state.page == "Home":
    st.markdown('<p class="main-title">📈 EconoLearn</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your economic adventure begins here!</p>', unsafe_allow_html=True)

    # Dashboard
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='card' style='text-align:center;'><b>XP</b><br><h3>{st.session_state.xp}</h3></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='card' style='text-align:center;'><b>Level</b><br><span class='level-badge beginner'>{st.session_state.level}</span></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='card' style='text-align:center;'><b>Streak</b><br><h3>{st.session_state.streak} 🔥</h3></div>", unsafe_allow_html=True)

    st.markdown("### 🗺️ Choose a Topic")
    topic_cols = st.columns(5)
    for i, (t, icon) in enumerate(TOPICS.items()):
        with topic_cols[i % 5]:
            if st.button(f"{icon}\n{t}", key=f"btn_{t}"):
                st.session_state.topic = t
                st.session_state.page = "Daily Lesson"
                st.rerun()

elif st.session_state.page == "Daily Lesson":
    st.markdown(f"<p class='main-title'>{TOPICS.get(st.session_state.topic)} {st.session_state.topic}</p>", unsafe_allow_html=True)
    lesson = LESSONS.get(st.session_state.topic, LESSONS["Supply & Demand"]).get("Beginner")
    st.markdown(f"<div class='card'><b>{lesson['title']}</b><br><br>{lesson['content']}</div>", unsafe_allow_html=True)
    if st.button("← Back to Map"):
        st.session_state.page = "Home"
        st.rerun()

elif st.session_state.page == "Quiz":
    st.markdown("<p class='main-title'>❓ Quiz Time</p>", unsafe_allow_html=True)
    st.markdown("<div class='card'>Test your knowledge! (Quiz module loading...)</div>", unsafe_allow_html=True)
    if st.button("← Back to Map"):
        st.session_state.page = "Home"
        st.rerun()
