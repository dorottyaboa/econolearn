import streamlit as st
import random
import json
import hashlib
from datetime import datetime, date

st.set_page_config(page_title="EconoLearn", page_icon="🎨", layout="wide")

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "level": "Beginner",
        "topic": "Supply & Demand",
        "page": "Home",
        "score": 0,
        "total_answered": 0,
        "correct_answered": 0,
        "streak": 0,
        "daily_done": set(),
        "quiz_answered": {},
        "fill_answers": {},
        "xp": 0,
        "badges": [],
        "history_idx": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
# CSS OVERHAUL (FIXED COLORS & BUTTONS)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');

    /* Global Text & Background */
    html, body, [class*="st-emotion-cache"], .stApp {
        font-family: 'Nunito', sans-serif;
        background-color: #fffaf0 !important;
        color: #432818 !important; /* Dark Chocolate Brown for readability */
    }

    /* Force all text inside markdown to be dark */
    [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] h1, 
    [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] li, [data-testid="stMarkdownContainer"] span {
        color: #432818 !important;
    }

    .main-title { 
        font-size: 3.5rem; 
        font-weight: 800; 
        color: #ff85a2 !important; 
        text-shadow: 2px 2px 0px #ffe5ec;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .subtitle { 
        color: #6d6875 !important; 
        font-size: 1.3rem;
        text-align: center;
        font-weight: 700;
        margin-bottom: 2rem;
    }

    /* Comic Style Cards */
    .card { 
        background: #ffffff !important; 
        border-radius: 30px; 
        padding: 1.5rem; 
        margin-bottom: 1.5rem; 
        border: 4px solid #f1f2f6;
        box-shadow: 8px 8px 0px #e0e0e0;
    }
    .card b, .card span, .card h3 {
        color: #432818 !important;
    }
    
    .card-blue { border-color: #bae6fd !important; background: #f0f9ff !important; box-shadow: 8px 8px 0px #bae6fd; }
    .card-green { border-color: #bbf7d0 !important; background: #f0fdf4 !important; box-shadow: 8px 8px 0px #bbf7d0; }
    .card-red { border-color: #fecaca !important; background: #fef2f2 !important; box-shadow: 8px 8px 0px #fecaca; }
    .card-gold { border-color: #fef08a !important; background: #fefce8 !important; box-shadow: 8px 8px 0px #fef08a; }

    /* Fix Button Boxes & Colors */
    .stButton > button {
        border-radius: 30px !important;
        border: none !important;
        background-color: #ffb7b2 !important; 
        color: #ffffff !important;
        padding: 0.6rem 2rem !important;
        font-weight: 800 !important;
        box-shadow: 0px 5px 0px #ff8a8a !important;
        transition: all 0.1s ease !important;
        width: 100%;
        display: block;
    }
    
    /* Remove the white square/background from Streamlit button interiors */
    .stButton > button div {
        background-color: transparent !important;
        color: white !important;
    }
    
    .stButton > button:hover {
        transform: translateY(2px) !important;
        box-shadow: 0px 3px 0px #ff8a8a !important;
        background-color: #ff9aa2 !important;
    }

    /* Level Badge Stickers */
    .level-badge { 
        display: inline-block; 
        padding: 6px 18px; 
        border-radius: 20px; 
        font-size: 0.9rem; 
        font-weight: 800; 
        text-transform: uppercase;
        color: #ffffff !important;
    }
    .beginner { background: #0ea5e9 !important; }
    .intermediate { background: #f97316 !important; }
    .advanced { background: #84cc16 !important; }

    /* Sidebar Fixes */
    section[data-testid="stSidebar"] {
        background-color: #fff5f5 !important;
        border-right: 2px dashed #ffb7b2;
    }
    section[data-testid="stSidebar"] * {
        color: #432818 !important;
    }

    /* XP Bar */
    .xp-bar { background: #f1f2f6; border-radius: 50px; height: 22px; border: 3px solid #e2e8f0; overflow: hidden; }
    .xp-fill { background: linear-gradient(90deg, #ffb7b2, #ffdac1); height: 100%; border-radius: 50px; }

    /* Metric Fix */
    [data-testid="stMetricValue"] {
        color: #432818 !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #6d6875 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATABASE (TOPICS & LESSONS)
# ─────────────────────────────────────────────

LEVELS = ["Beginner", "Intermediate", "Advanced"]

TOPICS = {
    "Supply & Demand": "🛒",
    "Inflation & Deflation": "💸",
    "GDP & Growth": "📊",
    "Monetary Policy": "🏦",
    "Fiscal Policy": "🏛️",
    "Labor Markets": "👷",
    "Trade & Globalization": "🌍",
    "Financial Markets": "📉",
    "Business Cycles": "🔄",
    "Behavioral Economics": "🧠",
}

LESSONS = {
    "Supply & Demand": {
        "Beginner": {
            "title": "The Basics of Supply & Demand",
            "content": "**Supply and demand** is the foundation of economics. It explains how prices are set. \n\n **Demand**: People want to buy more when it's cheap. \n\n **Supply**: Makers want to sell more when it's expensive.",
        }
    },
    "Behavioral Economics": {
        "Beginner": {
            "title": "How Humans Think",
            "content": "Economics usually assumes people are logical. **Behavioral economics** shows that we are actually quite messy and biased!",
        }
    }
}

QUIZ_QUESTIONS = {"Beginner": [{"q": "What happens if demand rises?", "options": ["A) Price rises", "B) Price falls"], "answer": "A", "explanation": "More people wanting something makes it more valuable!"}]}

SCENARIO_EXERCISES = {"Beginner": [{"scenario": "The Toy Craze", "situation": "Everyone wants the new robot toy, but the factory only made 100.", "question": "Will the store raise or lower the price?", "answer": "Raise! This is a classic shortage.", "key_concept": "Scarcity"}]}

BADGE_ICONS = {"First 100 XP": "🥉", "Quiz Master": "🎓"}

def award_xp(amount, reason=""):
    st.session_state.xp += amount

def get_daily_topic():
    topic_list = list(TOPICS.keys())
    return topic_list[date.today().day % len(topic_list)]

# ─────────────────────────────────────────────
# UI - SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🎨 EconoLearn</h1>", unsafe_allow_html=True)
    st.markdown("---")

    xp = st.session_state.xp
    xp_level = min(xp // 100, 10)
    xp_progress = (xp % 100) / 100
    st.markdown(f"**Level {xp_level} Explorer** ✨")
    st.markdown(f"""<div class="xp-bar"><div class="xp-fill" style="width:{int(xp_progress*100)}%"></div></div>""", unsafe_allow_html=True)
    st.caption(f"{xp} XP Total")

    st.markdown("---")
    st.markdown("### 🗺️ Navigation")
    pages = ["Home", "Daily Lesson", "Quiz", "Scenarios", "My Progress"]
    for pg in pages:
        if st.button(pg, key=f"nav_{pg}"):
            st.session_state.page = pg

    st.markdown("---")
    st.markdown("### 🏆 Mastery")
    for lvl in LEVELS:
        if st.button(lvl, key=f"lvl_{lvl}"):
            st.session_state.level = lvl
    st.markdown(f"Active: <span class='level-badge beginner'>{st.session_state.level}</span>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# UI - PAGES
# ─────────────────────────────────────────────

page = st.session_state.page
level = st.session_state.level
topic = st.session_state.topic

if page == "Home":
    st.markdown('<p class="main-title">🎨 EconoLearn</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Master the world of money and choice!</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Total XP", st.session_state.xp)
    with col2: st.metric("Streak", f"{st.session_state.streak} days")
    with col3: st.metric("Accuracy", "100%")

    daily_topic = get_daily_topic()
    st.markdown(f"### 📬 Today's Challenge: {TOPICS[daily_topic]} {daily_topic}")
    
    st.markdown(f"<div class='card card-blue'><b>Ready for a new adventure?</b><br>Today we are diving into {daily_topic}!</div>", unsafe_allow_html=True)
    if st.button("Start Quest →", key="start_quest"):
        st.session_state.page = "Daily Lesson"
        st.session_state.topic = daily_topic
        st.rerun()

    st.markdown("---")
    st.markdown("### 🗺️ Explore All Topics")
    topic_cols = st.columns(5)
    for i, (t, icon) in enumerate(TOPICS.items()):
        with topic_cols[i % 5]:
            if st.button(f"{icon}\n{t}", key=f"topic_{t}"):
                st.session_state.topic = t
                st.session_state.page = "Daily Lesson"
                st.rerun()

elif page == "Daily Lesson":
    lesson = LESSONS.get(topic, {}).get(level, LESSONS["Supply & Demand"]["Beginner"])
    st.markdown(f"## {TOPICS.get(topic, '')} {lesson['title']}")
    st.markdown(f"<div class='card'>{lesson['content']}</div>", unsafe_allow_html=True)
    if st.button("Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

elif page == "Quiz":
    st.markdown(f"## ❓ Brain Tickler")
    q = QUIZ_QUESTIONS["Beginner"][0]
    st.markdown(f"<div class='card'><b>Question:</b> {q['q']}</div>", unsafe_allow_html=True)
    for opt in q['options']:
        if st.button(opt):
            st.success("Correct! +15 XP")
            award_xp(15)

elif page == "Scenarios":
    st.markdown("## 🎯 Real World Puzzles")
    s = SCENARIO_EXERCISES["Beginner"][0]
    st.markdown(f"<div class='card card-gold'><b>{s['scenario']}</b><br>{s['situation']}</div>", unsafe_allow_html=True)
    if st.button("Reveal Answer ✨"):
        st.info(s['answer'])

elif page == "My Progress":
    st.markdown("## 📊 My Sticker Book")
    st.markdown(f"<div class='card'><h3>XP: {st.session_state.xp}</h3></div>", unsafe_allow_html=True)
    if st.button("Clear Progress"):
        st.session_state.xp = 0
        st.rerun()
