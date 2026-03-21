import streamlit as st
import random
import hashlib
from datetime import date

st.set_page_config(page_title="EconoLearn", page_icon="📈", layout="wide")

# ─────────────────────────────────────────────
# CONTENT DATABASE
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
            "content": """
**Supply and demand** is the foundation of economics. It explains how prices are set and how resources are allocated.

### Demand
- **Demand** is the amount of a good or service consumers are *willing and able* to buy at different prices.
- **Law of Demand**: When price rises, quantity demanded falls (inverse relationship).

### Supply
- **Supply** is the amount of a good or service producers are *willing and able* to sell at different prices.
- **Law of Supply**: When price rises, quantity supplied increases (positive relationship).

### Equilibrium
- **Equilibrium** is where supply meets demand — the price at which the market clears.
            """,
            "key_terms": {"Demand": "Willingness and ability to buy", "Supply": "Willingness and ability to sell", "Equilibrium": "Price where supply equals demand"},
        },
        "Intermediate": {
            "title": "Elasticity & Market Shifts",
            "content": """
### Price Elasticity of Demand (PED)
Elasticity measures *how responsive* quantity is to a price change.
            """,
            "key_terms": {"Elasticity": "Responsiveness of quantity to price changes"},
        },
        "Advanced": {
            "title": "Market Failures & Externalities",
            "content": """
### When Markets Fail
Free markets are efficient *only* under perfect conditions.
            """,
            "key_terms": {"Externality": "Cost/benefit falling on third parties"},
        },
    },
}

QUIZ_QUESTIONS = {
    "Beginner": [
        {"q": "What happens to the price of a good when supply decreases and demand stays the same?", "options": ["A) Price falls", "B) Price rises", "C) Price stays the same", "D) Quantity demanded falls to zero"], "answer": "B", "explanation": "With the same demand but less supply, the equilibrium price rises."},
    ],
}

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────

if "xp" not in st.session_state:
    st.session_state.xp = 0
if "level" not in st.session_state:
    st.session_state.level = "Beginner"
if "topic" not in st.session_state:
    st.session_state.topic = "Supply & Demand"

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.title("📈 EconoLearn")
    st.write(f"**XP:** {st.session_state.xp}")
    st.session_state.level = st.selectbox("Select Level", LEVELS, index=LEVELS.index(st.session_state.level))
    st.session_state.topic = st.selectbox("Select Topic", list(TOPICS.keys()), index=list(TOPICS.keys()).index(st.session_state.topic))

# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────

st.title(f"{TOPICS[st.session_state.topic]} {st.session_state.topic}")

lesson = LESSONS.get(st.session_state.topic, {}).get(st.session_state.level)

if lesson:
    st.header(lesson["title"])
    st.markdown(lesson["content"])
    
    with st.expander("🔑 Key Terms"):
        for term, definition in lesson["key_terms"].items():
            st.write(f"**{term}**: {definition}")

    if st.button("I've read this! (+10 XP)"):
        st.session_state.xp += 10
        st.success("XP Earned!")
else:
    st.info("Lesson content coming soon for this level!")

st.divider()

st.subheader("❓ Quick Quiz")
questions = QUIZ_QUESTIONS.get(st.session_state.level, [])
if questions:
    q = questions[0]
    st.write(q["q"])
    ans = st.radio("Choose one:", q["options"], key="quiz_radio")
    if st.button("Submit Answer"):
        if ans.startswith(q["answer"]):
            st.success("Correct! +15 XP")
            st.session_state.xp += 15
        else:
            st.error(f"Wrong. {q['explanation']}")
