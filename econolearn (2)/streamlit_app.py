import streamlit as st
import pandas as pd
import json
import time

st.set_page_config(page_title="EconoLearn", page_icon="📈", layout="centered")

# --- DATA PORTED FROM CONSTANTS.TS ---
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

UNITS = [
    {
        "id": "unit-1",
        "title": "Unit 1: The Core Foundation",
        "description": "Master the fundamental principles of supply, demand, and market equilibrium.",
        "level": "Beginner",
        "nodes": [
            {"id": "node-1", "title": "Supply & Demand 101", "topic": "Supply & Demand", "level": "Beginner", "icon": "🛒"},
            {"id": "node-2", "title": "Inflation Basics", "topic": "Inflation & Deflation", "level": "Beginner", "icon": "💸"},
            {"id": "node-3", "title": "Understanding GDP", "topic": "GDP & Growth", "level": "Beginner", "icon": "📊"},
        ]
    },
    {
        "id": "unit-2",
        "title": "Unit 2: Policy & Power",
        "description": "Explore how governments and central banks influence the economy.",
        "level": "Beginner",
        "nodes": [
            {"id": "node-4", "title": "Monetary Policy Intro", "topic": "Monetary Policy", "level": "Beginner", "icon": "🏦"},
            {"id": "node-5", "title": "Fiscal Policy Intro", "topic": "Fiscal Policy", "level": "Beginner", "icon": "🏛️"},
            {"id": "node-6", "title": "Labor Markets 101", "topic": "Labor Markets", "level": "Beginner", "icon": "👷"},
        ]
    },
    {
        "id": "unit-3",
        "title": "Unit 3: Global Connections",
        "description": "Learn how countries trade and how markets fluctuate over time.",
        "level": "Beginner",
        "nodes": [
            {"id": "node-7", "title": "Trade & Globalization", "topic": "Trade & Globalization", "level": "Beginner", "icon": "🌍"},
            {"id": "node-8", "title": "Financial Markets Intro", "topic": "Financial Markets", "level": "Beginner", "icon": "📉"},
            {"id": "node-9", "title": "Business Cycles Intro", "topic": "Business Cycles", "level": "Beginner", "icon": "🔄"},
            {"id": "node-10", "title": "Behavioral Economics Intro", "topic": "Behavioral Economics", "level": "Beginner", "icon": "🧠"},
        ]
    },
    {
        "id": "unit-4",
        "title": "Unit 4: Intermediate Dynamics",
        "description": "Deep dive into elasticity, market shifts, and the Fisher effect.",
        "level": "Intermediate",
        "nodes": [
            {"id": "node-11", "title": "Elasticity & Shifts", "topic": "Supply & Demand", "level": "Intermediate", "icon": "🛒"},
            {"id": "node-12", "title": "The Fisher Effect", "topic": "Inflation & Deflation", "level": "Intermediate", "icon": "💸"},
            {"id": "node-13", "title": "Growth Models", "topic": "GDP & Growth", "level": "Intermediate", "icon": "📊"},
        ]
    },
    {
        "id": "unit-5",
        "title": "Unit 5: Advanced Macro",
        "description": "Master the IS-LM model, ZLB, and complex market design.",
        "level": "Advanced",
        "nodes": [
            {"id": "node-14", "title": "IS-LM Model", "topic": "Monetary Policy", "level": "Advanced", "icon": "🏦"},
            {"id": "node-15", "title": "ZLB & Fiscal", "topic": "Fiscal Policy", "level": "Advanced", "icon": "🏛️"},
            {"id": "node-16", "title": "Game Theory", "topic": "Behavioral Economics", "level": "Advanced", "icon": "🧠"},
        ]
    },
]

LESSONS = {
    "Supply & Demand": {
        "Beginner": {
            "title": "The Basics of Supply & Demand",
            "content": """**Supply and demand** is the foundation of economics. It explains how prices are set and how resources are allocated.

### Demand
- **Demand** is the amount of a good or service consumers are *willing and able* to buy at different prices.
- **Law of Demand**: When price rises, quantity demanded falls (inverse relationship).
- Think of it like this: if pizza costs $50, you'd buy less of it than if it costs $5.

### Supply
- **Supply** is the amount of a good or service producers are *willing and able* to sell at different prices.
- **Law of Supply**: When price rises, quantity supplied increases (positive relationship).
- Higher prices = more profit motive = more production.

### Equilibrium
- **Equilibrium** is where supply meets demand — the price at which the market clears.
- If price is *above* equilibrium → **surplus** (excess supply).
- If price is *below* equilibrium → **shortage** (excess demand).

### Real-World Example
After a hurricane destroys orange groves in Florida, **supply of oranges drops**. With the same demand but less supply, prices rise — this is why OJ gets expensive after storms.""",
            "key_terms": {
                "Demand": "Willingness and ability to buy at a given price",
                "Supply": "Willingness and ability to sell at a given price",
                "Equilibrium": "Price where quantity supplied equals quantity demanded",
                "Surplus": "When supply exceeds demand at a given price",
                "Shortage": "When demand exceeds supply at a given price",
            }
        },
        "Intermediate": {
            "title": "Elasticity & Market Shifts",
            "content": """### Price Elasticity of Demand (PED)
How sensitive are consumers to price changes?
- **Elastic (|PED| > 1)**: Small price change = big quantity change (e.g., luxury cars).
- **Inelastic (|PED| < 1)**: Big price change = small quantity change (e.g., insulin, gasoline).

### Determinants of Elasticity
1. **Substitutes**: More substitutes = more elastic.
2. **Necessity vs. Luxury**: Necessities are inelastic.
3. **Time**: Demand is more elastic in the long run.

### Market Shifts
- **Shift in Demand**: Caused by income, tastes, or price of related goods (substitutes/complements).
- **Shift in Supply**: Caused by input prices, technology, or expectations.""",
            "key_terms": {
                "Elasticity": "Measure of responsiveness to price changes",
                "Substitute": "A good that can be used in place of another",
                "Complement": "A good used together with another",
                "Normal Good": "Demand rises when income rises",
                "Inferior Good": "Demand falls when income rises",
            }
        }
    },
    "Inflation & Deflation": {
        "Beginner": {
            "title": "Inflation Basics",
            "content": """**Inflation** is the general increase in prices and fall in the purchasing value of money.

### Why does it happen?
1. **Demand-Pull**: "Too much money chasing too few goods."
2. **Cost-Push**: Rising production costs (like oil) push prices up.
3. **Monetary Expansion**: Central bank prints too much money.

### How is it measured?
- **CPI (Consumer Price Index)**: A "basket" of goods an average family buys.
- **Deflation**: When prices fall (sounds good, but can lead to economic stagnation).""",
            "key_terms": {
                "Inflation": "General rise in price level",
                "Deflation": "General fall in price level",
                "CPI": "Consumer Price Index",
                "Purchasing Power": "The value of money in terms of what it can buy",
            }
        }
    }
}

QUIZ_QUESTIONS = {
    "Beginner": [
        {
            "q": "What happens to the price of a good when supply decreases and demand stays the same?",
            "options": ["A) Price falls", "B) Price rises", "C) Price stays the same", "D) Quantity demanded falls to zero"],
            "answer": "B",
            "explanation": "With the same demand but less supply, the equilibrium price rises — there are fewer goods competing for the same buyers."
        }
    ]
}

SCENARIO_EXERCISES = {
    "Beginner": [
        {
            "scenario": "🌽 The Corn Crisis",
            "situation": "A drought destroys 40% of the US corn crop. Corn is used in food, animal feed, and ethanol fuel.",
            "question": "What do you predict will happen to: (1) the price of corn, (2) the price of beef, and (3) the price of gasoline?",
            "answer": "1. Corn price RISES (supply decreased, demand unchanged → shortage → higher price). 2. Beef price RISES (corn = cow feed → input cost rises → supply of beef shifts left → price rises). 3. Gasoline price RISES (ethanol is a substitute/blend for gasoline; if corn is scarce, ethanol is scarce, and gasoline demand rises). This is called a 'supply chain ripple effect.'",
            "key_concept": "Supply shocks ripple through interconnected markets via input costs and substitutes."
        }
    ]
}

HISTORY_EVENTS = [
    {
        "year": "1776",
        "event": "The Wealth of Nations",
        "description": "Adam Smith publishes *The Wealth of Nations*, founding modern economics. Key ideas: division of labor, the 'invisible hand' of markets, free trade over mercantilism.",
        "lesson": "Markets can coordinate complex activity without central direction through price signals.",
        "era": "Classical Economics"
    }
]

# --- SESSION STATE INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 3
if 'darkMode' not in st.session_state: st.session_state.darkMode = False
if 'completedNodes' not in st.session_state: st.session_state.completedNodes = []
if 'page' not in st.session_state: st.session_state.page = "Home"
if 'topic' not in st.session_state: st.session_state.topic = "Supply & Demand"
if 'level' not in st.session_state: st.session_state.level = "Beginner"
if 'quizAnswers' not in st.session_state: st.session_state.quizAnswers = {}
if 'scenarioRevealed' not in st.session_state: st.session_state.scenarioRevealed = {}

# --- THEME COLORS ---
LIGHT_THEME = {
    "bg": "#f9f6e3",
    "text": "#2d2020",
    "card": "#dbe8cd",
    "card_b": "#b8c4a4",
    "sidebar": "#6aa08f",
    "btn": "#e8ae7d",
    "btn_sh": "#a56066",
    "accent": "#6aa08f"
}

DARK_THEME = {
    "bg": "#1e1c2e",
    "text": "#e3e1c8",
    "card": "#514d86",
    "card_b": "#816cb1",
    "sidebar": "#16142a",
    "btn": "#d289ae",
    "btn_sh": "#8a4a6e",
    "accent": "#c5c5ff"
}

theme = DARK_THEME if st.session_state.darkMode else LIGHT_THEME

# --- CUSTOM CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    .stApp {{
        background-color: {theme['bg']};
        color: {theme['text']};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Top Bar */
    .top-bar {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background-color: {theme['sidebar']};
        border-bottom: 4px solid {theme['card_b']};
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 24px;
        color: white;
    }}
    
    .top-bar h2 {{
        font-weight: 900;
        letter-spacing: -1px;
        margin: 0;
        font-size: 24px;
    }}
    
    .stat-pill {{
        background: rgba(255,255,255,0.1);
        padding: 4px 12px;
        border-radius: 20px;
        border: 2px solid rgba(255,255,255,0.2);
        font-weight: 900;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    
    /* Bottom Nav */
    .bottom-nav {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 80px;
        background-color: {theme['sidebar']};
        border-top: 4px solid {theme['card_b']};
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: space-around;
        padding: 0 16px;
    }}
    
    .nav-item {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        color: rgba(255,255,255,0.4);
        text-decoration: none;
        cursor: pointer;
        background: none;
        border: none;
    }}
    
    .nav-item.active {{
        color: white;
        transform: scale(1.1);
    }}
    
    .nav-icon {{
        font-size: 24px;
        padding: 8px;
        border-radius: 12px;
    }}
    
    .nav-item.active .nav-icon {{
        background: rgba(255,255,255,0.2);
        border: 2px solid rgba(255,255,255,0.3);
    }}
    
    .nav-label {{
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Map Layout */
    .map-container {{
        max-width: 450px;
        margin: 80px auto 100px auto;
        padding: 0 16px;
    }}
    
    .unit-card {{
        background-color: {theme['card']};
        border: 4px solid {theme['card_b']};
        border-radius: 32px;
        padding: 24px;
        margin-bottom: 64px;
        box-shadow: 8px 8px 0 rgba(0,0,0,0.1);
        position: relative;
    }}
    
    .unit-card h3 {{
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 3px;
        opacity: 0.7;
        margin-bottom: 4px;
    }}
    
    .unit-card h2 {{
        font-size: 24px;
        font-weight: 900;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }}
    
    .unit-card p {{
        font-size: 14px;
        font-weight: 500;
        opacity: 0.9;
        line-height: 1.2;
    }}
    
    .path-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 64px;
        position: relative;
    }}
    
    .path-line {{
        position: absolute;
        top: 0;
        bottom: 0;
        width: 12px;
        background-color: {theme['sidebar'] if st.session_state.darkMode else 'rgba(0,0,0,0.1)'};
        z-index: -1;
        border-radius: 6px;
    }}
    
    .node-btn {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: none;
        border-bottom: 8px solid;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        cursor: pointer;
        transition: all 0.2s;
        position: relative;
    }}
    
    .node-btn.completed {{
        background-color: {theme['btn']};
        border-color: {theme['btn_sh']};
        color: white;
    }}
    
    .node-btn.unlocked {{
        background-color: white;
        border-color: #ccc;
        color: #333;
    }}
    
    .node-btn.locked {{
        background-color: #eee;
        border-color: #ccc;
        color: #999;
        opacity: 0.5;
        cursor: not-allowed;
    }}
    
    .node-label {{
        position: absolute;
        top: 100%;
        margin-top: 16px;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
        padding: 4px 12px;
        border-radius: 12px;
        border: 2px solid {theme['card_b']};
        background: {theme['card']};
        font-weight: 900;
        text-transform: uppercase;
        font-size: 9px;
        letter-spacing: 1px;
    }}
    
    .check-mark {{
        position: absolute;
        top: -4px;
        right: -4px;
        background: #22c55e;
        color: white;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        border: 2px solid white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    
    /* Hide Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
</style>
""", unsafe_allow_html=True)

# --- RENDERERS ---

def render_top_bar():
    cols = st.columns([1, 2, 1])
    with cols[0]:
        st.markdown(f"""
        <div style="display: flex; gap: 8px;">
            <div class="stat-pill">🔥 {st.session_state.streak}</div>
            <div class="stat-pill">🏆 {st.session_state.xp}</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("<h2 style='text-align: center; font-weight: 900; letter-spacing: -1px;'>📈 ECONO</h2>", unsafe_allow_html=True)
    with cols[2]:
        if st.button("☀️" if st.session_state.darkMode else "🌙", key="theme_toggle", use_container_width=True):
            st.session_state.darkMode = not st.session_state.darkMode
            st.rerun()

    st.markdown("<hr style='margin: 10px 0; opacity: 0.2;'>", unsafe_allow_html=True)

def render_bottom_nav():
    items = [
        {"icon": "🗺️", "label": "Map", "id": "Home"},
        {"icon": "❓", "label": "Quiz", "id": "Quiz"},
        {"icon": "🎯", "label": "Scenarios", "id": "Scenarios"},
        {"icon": "📜", "label": "History", "id": "History"},
        {"icon": "📊", "label": "Stats", "id": "Stats"},
    ]
    
    cols = st.columns(len(items))
    for i, item in enumerate(items):
        with cols[i]:
            active = "active" if st.session_state.page == item['id'] else ""
            if st.button(f"{item['icon']}\n{item['label']}", key=f"nav_{item['id']}", use_container_width=True):
                st.session_state.page = item['id']
                st.rerun()

def render_map():
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    
    for unit_idx, unit in enumerate(UNITS):
        st.markdown(f"""
        <div class="unit-card">
            <h3>Unit {unit_idx + 1}</h3>
            <h2>{unit['title']}</h2>
            <p>{unit['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="path-container">', unsafe_allow_html=True)
        st.markdown('<div class="path-line"></div>', unsafe_allow_html=True)
        
        for node_idx, node in enumerate(unit['nodes']):
            # Unlock logic
            all_nodes = [n for u in UNITS for n in u['nodes']]
            node_index_global = all_nodes.index(node)
            unlocked = True if node_index_global == 0 else (all_nodes[node_index_global-1]['id'] in st.session_state.completedNodes)
            completed = node['id'] in st.session_state.completedNodes
            
            # S-curve offset using columns
            # positions = [0, 70, 0, -70]
            # We'll use 5 columns to simulate this: [col3, col4, col3, col2]
            col_layouts = [
                [1, 1, 2, 1, 1], # Center
                [1, 1, 1, 2, 1], # Right
                [1, 1, 2, 1, 1], # Center
                [1, 2, 1, 1, 1], # Left
            ]
            layout = col_layouts[node_idx % 4]
            cols = st.columns(layout)
            
            # Find the "active" column (the one with width 2)
            active_col_idx = layout.index(2)
            
            with cols[active_col_idx]:
                status_icon = "✅" if completed else ("🔓" if unlocked else "🔒")
                if st.button(f"{node['icon']}\n{status_icon}", key=f"node_{node['id']}", disabled=not unlocked, use_container_width=True):
                    st.session_state.topic = node['topic']
                    st.session_state.level = node['level']
                    st.session_state.page = "Lesson"
                    st.rerun()
                st.markdown(f"<div style='text-align: center; font-size: 10px; font-weight: 900; margin-top: -10px;'>{node['title']}</div>", unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="height: 64px;"></div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_lesson():
    topic = st.session_state.topic
    level = st.session_state.level
    lesson = LESSONS.get(topic, {}).get(level)
    
    if not lesson:
        st.warning("Lesson not found.")
        if st.button("Back to Map"):
            st.session_state.page = "Home"
            st.rerun()
        return

    st.markdown(f"<h1 style='text-align: center; font-weight: 900;'>{lesson['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; margin-bottom: 32px;'><span style='background: #eee; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 900; color: #333;'>{level}</span></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: {theme['card']}; border: 4px solid {theme['card_b']}; border-radius: 32px; padding: 32px; margin-bottom: 32px; color: {theme['text']};">
        {lesson['content']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔑 Key Terms")
    cols = st.columns(2)
    for i, (term, defn) in enumerate(lesson['key_terms'].items()):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background: {theme['sidebar']}; color: white; padding: 16px; border-radius: 16px; margin-bottom: 16px;">
                <b style="display: block; margin-bottom: 4px;">{term}</b>
                <span style="font-size: 12px; opacity: 0.8;">{defn}</span>
            </div>
            """, unsafe_allow_html=True)
            
    if st.button("Complete Lesson & Return to Map", use_container_width=True):
        # Find node ID
        node = next((n for u in UNITS for n in u['nodes'] if n['topic'] == topic and n['level'] == level), None)
        if node and node['id'] not in st.session_state.completedNodes:
            st.session_state.completedNodes.append(node['id'])
            st.session_state.xp += 50
        st.session_state.page = "Home"
        st.rerun()

def render_quiz():
    st.markdown("<h1 style='text-align: center; font-weight: 900;'>Quiz Time!</h1>", unsafe_allow_html=True)
    questions = QUIZ_QUESTIONS.get(st.session_state.level, [])
    
    for i, q in enumerate(questions):
        st.markdown(f"### {q['q']}")
        for opt in q['options']:
            if st.button(opt, key=f"q_{i}_{opt}"):
                if opt.startswith(q['answer']):
                    st.success(f"Correct! {q['explanation']}")
                    st.session_state.xp += 10
                else:
                    st.error(f"Incorrect. {q['explanation']}")

def render_scenarios():
    st.markdown("<h1 style='text-align: center; font-weight: 900;'>Economic Scenarios</h1>", unsafe_allow_html=True)
    scenarios = SCENARIO_EXERCISES.get(st.session_state.level, [])
    
    for i, s in enumerate(scenarios):
        st.markdown(f"## {s['scenario']}")
        st.info(s['situation'])
        st.markdown(f"**Question:** {s['question']}")
        
        if st.button("Reveal Answer", key=f"scenario_{i}"):
            st.success(s['answer'])
            st.info(f"**Key Concept:** {s['key_concept']}")
            st.session_state.xp += 5

def render_history():
    st.markdown("<h1 style='text-align: center; font-weight: 900;'>Economic History</h1>", unsafe_allow_html=True)
    for event in HISTORY_EVENTS:
        st.markdown(f"## {event['year']}: {event['event']}")
        st.markdown(f"*{event['era']}*")
        st.write(event['description'])
        st.info(f"💡 **Lesson:** {event['lesson']}")

def render_stats():
    st.markdown("<h1 style='text-align: center; font-weight: 900;'>Your Progress</h1>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    stats = [
        {"label": "Total XP", "value": st.session_state.xp},
        {"label": "Streak", "value": f"{st.session_state.streak} days"},
        {"label": "Lessons", "value": len(st.session_state.completedNodes)},
        {"label": "Level", "value": st.session_state.level},
    ]
    
    for i, stat in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align: center; background: {theme['card']}; padding: 16px; border-radius: 24px; border: 4px solid {theme['card_b']};">
                <div style="font-size: 10px; font-weight: 900; opacity: 0.5;">{stat['label']}</div>
                <div style="font-size: 20px; font-weight: 900;">{stat['value']}</div>
            </div>
            """, unsafe_allow_html=True)

    if st.button("Reset All Progress", type="secondary"):
        st.session_state.xp = 0
        st.session_state.completedNodes = []
        st.session_state.page = "Home"
        st.rerun()

# --- MAIN APP LOGIC ---
render_top_bar()

if st.session_state.page == "Home":
    render_map()
elif st.session_state.page == "Lesson":
    render_lesson()
elif st.session_state.page == "Quiz":
    render_quiz()
elif st.session_state.page == "Scenarios":
    render_scenarios()
elif st.session_state.page == "History":
    render_history()
elif st.session_state.page == "Stats":
    render_stats()

st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
render_bottom_nav()
