# SQL Practice App (Beginner) — SQLite

A beginner-friendly Streamlit app to practice SQL using a built-in SQLite database.

## Run locally

1) (Optional) Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Start the app:

```bash
streamlit run app.py
```

The app auto-creates `learn_sql.db` on first run.

## Deploy on Railway

This project includes `Procfile`, `railway.toml`, and `runtime.txt`.

1) Push this repo to GitHub.
2) In Railway, create a new project from the repo.
3) Deploy. Railway will run:
`streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

## GitHub SSH setup (optional)

If you prefer SSH for GitHub pushes:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub
```

Add the public key to your GitHub account, then use:

```bash
git remote set-url origin git@github.com:adarshdessai4-spec/sql_learn.git
```
