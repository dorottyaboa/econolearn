# EconoLearn 📈

An interactive economics learning app built with Streamlit. Learn how the economy works through daily lessons, quizzes, and exercises — from beginner to advanced. Progress is saved to your account.

## Features

- **Login / Register** — Email & password, or Continue with Google / Apple
- **Progress Saving** — XP, badges, streaks, and quiz results saved per user
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

## Configure OAuth (optional)

Create `.streamlit/secrets.toml` in the project root:

```toml
[google]
client_id     = "your-google-client-id"
client_secret = "your-google-client-secret"
redirect_uri  = "http://localhost:8501"   # or your deployed URL

[apple]
client_id   = "com.your.serviceid"
team_id     = "YOUR_TEAM_ID"
key_id      = "YOUR_KEY_ID"
private_key = """-----BEGIN PRIVATE KEY-----
...your ES256 key...
-----END PRIVATE KEY-----"""
redirect_uri = "http://localhost:8501"
```

Without these, email/password registration and login still work fully.

For Google: create credentials at [console.cloud.google.com](https://console.cloud.google.com) → OAuth 2.0 Client IDs → Web application. Add your app URL as an authorised redirect URI.

For Apple: requires an Apple Developer account. Create a Services ID and a Sign In with Apple key at [developer.apple.com](https://developer.apple.com).

## Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo and set `app.py` as the entry point
4. Add your OAuth secrets in the **Secrets** tab in the Streamlit Cloud dashboard
5. Update `redirect_uri` values to your `https://your-app.streamlit.app` URL

## Database

User accounts and progress are stored in `econolearn.db` (SQLite) next to `app.py`. On Streamlit Cloud this file is ephemeral — for persistent storage across deploys, migrate the DB to a hosted service (e.g. Supabase, PlanetScale).

## Requirements

- Python 3.8+
- streamlit >= 1.32.0
- requests >= 2.31.0
- PyJWT >= 2.8.0 (Apple Sign In)
- cryptography >= 42.0.0 (Apple Sign In)
