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
# CSS OVERHAUL (DARK GREEN SIDEBAR & NO SQUARES)
# ─────────────────────────────────────────────
# Colors: Dark Green Sidebar | Vanilla BG | Melon Buttons | Old Rose Text
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');

    /* Global App Background (Vanilla) */
    html, body, [class*="st-emotion-cache"], .stApp {
        font-family: 'Nunito', sans-serif;
        background-color: #FDF1A8 !important;
        color: #2D1B1E !important; 
    }

    /* 🌲 DARK GREEN SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #1b4332 !important; /* Deep Forest Green */
        border-right: 5px solid #B17C82;
    }
    
    /* Sidebar Text (Vanilla) */
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #FDF1A8 !important;
        font-weight: 700;
    }

    /* Comic Style Cards (Straw background) */
    .card { 
        background: #D3DC92 !important; 
        border-radius: 30px; 
        padding: 1.5rem; 
        margin-bottom: 1.5rem; 
        border: 5px solid #A4BD84;
        box-shadow: 10px 10px 0px #B17C82; 
    }
    
    .card b, .card span, .card h3, .card p {
        color: #2D1B1E !important;
    }

    /* 🎯 BUTTON FIX: No white squares, no keyboard icons, BOLD text */
    .stButton > button {
        border-radius: 25px !important;
        border: none !important;
        background-color: #FCAB92 !important; /* Melon */
        padding: 0.8rem 1rem !important;
        box-shadow: 0px 6px 0px #B17C82 !important; /* Old Rose */
        transition: all 0.1s ease !important;
        width: 100% !important;
        min-height: 85px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Kill the white boxes and keyboard labels inside buttons */
    .stButton > button div, 
    .stButton > button p, 
    .stButton > button span,
    .stButton > button div[data-testid="stMarkdownContainer"],
    .stButton > button div[data-testid="stButton-label"] {
        background-color: transparent !important;
        background: transparent !important;
        color: #2D1B1E !important; /* Dark text */
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        border: none !important;
        box-shadow: none !important;
        line-height: 1.2 !important;
    }

    /* Absolutely hide the keyboard shortcut/double icon */
    .stButton > button small, 
    .stButton > button svg,
    .stButton > button span[data-testid="stShortcut"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(2px) !important;
        box-shadow: 0px 3px 0px #B17C82 !important;
        background-color: #FCAB92 !important;
        filter: brightness(0.9);
    }

    .main-title { 
        font-size: 3.5rem; font-weight: 800; color: #B17C82 !important; 
        text-shadow: 3px 3px 0px #A4BD84; text-align: center;
    }
    
    .subtitle { 
        color: #1b4332 !important; font-size: 1.3rem; text-align: center;
        font-weight: 800; margin-bottom: 2rem;
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

# ─────────────────────────────────────────────
# MAIN PAGES
# ─────────────────────────────────────────────
if st.session_state.page == "Home":
    st.markdown('<p class="main-title">📈 EconoLearn</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Master the world of money!</p>', unsafe_allow_html=True)

    # Dashboard
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='card' style='text-align:center;'><b>XP</b><br><h3>{st.session_state.xp}</h3></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='card' style='text-align:center;'><b>Level</b><br><span class='level-badge beginner'>{st.session_state.level}</span></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='card' style='text-align:center;'><b>Streak</b><br><h3>{st.session_state.streak} 🔥</h3></div>", unsafe_allow_html=True)

    st.markdown("### 🗺️ Choose a Topic")
    topic_cols = st.columns(5)
    for i, (t, icon) in enumerate(TOPICS.items()):
        with topic_cols[i % 5]:
            # Labels are bolded and emojis included
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
    st.markdown("<div class='card'>Quiz module loading...</div>", unsafe_allow_html=True)
    if st.button("← Back to Map"):
        st.session_state.page = "Home"
        st.rerun()
