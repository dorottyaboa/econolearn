import streamlit as st
import random
import hashlib
from datetime import date

st.set_page_config(page_title="EconoLearn", page_icon="📈", layout="wide")

# CONTENT DATABASE
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

# ... (Original content from your Streamlit code)
# This file is provided for your reference so you can run it locally with Streamlit.
# The React version in this project uses the same data and logic.
