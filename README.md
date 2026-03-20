# EconoLearn 📈

An interactive economics learning app built with Streamlit. Learn how the economy works through daily lessons, quizzes, and exercises — from beginner to advanced.

## Features

- **3 Difficulty Levels** — Beginner, Intermediate, Advanced
- **Multiple Exercise Types** — Quizzes, fill-in-the-blank, scenarios, concept chains
- **Daily Lessons** — A new topic every day, rotating automatically
- **Economic History Timeline** — Key events from 1776 to today
- **XP & Badge System** — Earn XP and badges as you progress
- **Light & Dark Mode** — Toggle between themes at any time
- **Luxurious Design** — Playfair Display headings, soft shadows, gradient cards

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo and set `app.py` as the entry point
4. Add your OAuth secrets in the **Secrets** tab in the Streamlit Cloud dashboard
5. Update `redirect_uri` values to your `https://your-app.streamlit.app` URL

## Requirements

- Python 3.8+
- streamlit >= 1.32.0
- requests >= 2.31.0
- PyJWT >= 2.8.0 (Apple Sign In)
- cryptography >= 42.0.0 (Apple Sign In)
