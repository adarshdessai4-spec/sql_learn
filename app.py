import os
import sqlite3

import pandas as pd
import streamlit as st

DB_FILE = "learn_sql.db"

EXAMPLES = {
    "Show all users": "SELECT * FROM users;",
    "Users from Goa": "SELECT * FROM users WHERE city='Goa';",
    "Orders by Adarsh": """SELECT o.*
FROM orders o
JOIN users u ON u.id = o.user_id
WHERE u.name = 'Adarsh';""",
    "Latest 3 orders": "SELECT * FROM orders ORDER BY created_at DESC LIMIT 3;",
    "Total PAID amount": """SELECT SUM(amount) AS total_paid
FROM orders
WHERE status='PAID';""",
    "Orders with customer name (JOIN)": """SELECT o.id, u.name, o.amount, o.status, o.created_at
FROM orders o
JOIN users u ON u.id = o.user_id
ORDER BY o.created_at DESC;""",
    "Count users per city": """SELECT city, COUNT(*) AS total
FROM users
GROUP BY city;""",
}

EXERCISES = [
    "Show all users",
    "Show users from Goa",
    "Show orders where amount > 1000",
    "Show all orders by Pranjali",
    "Show total PAID amount",
    "Count users by city",
    "Show top 2 highest orders",
]


def get_connection():
    return sqlite3.connect(DB_FILE)


def reset_db():
    # Recreate tables and seed data for a fresh practice environment.
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS orders")
        cur.execute("DROP TABLE IF EXISTS users")

        cur.execute(
            """
            CREATE TABLE users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                city TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )

        users = [
            ("Adarsh", "adarsh@mail.com", "Goa"),
            ("Pranjali", "pranjali@mail.com", "Mumbai"),
            ("Rahul", "rahul@mail.com", "Pune"),
            ("Amit", "amit@mail.com", "Delhi"),
        ]
        cur.executemany("INSERT INTO users (name, email, city) VALUES (?, ?, ?)", users)

        cur.execute("SELECT id, name FROM users")
        id_map = {name: user_id for user_id, name in cur.fetchall()}

        orders = [
            (id_map["Adarsh"], 500, "PAID", "2026-01-10"),
            (id_map["Adarsh"], 999, "PENDING", "2026-01-11"),
            (id_map["Pranjali"], 1299, "PAID", "2026-01-11"),
            (id_map["Rahul"], 2500, "CANCELLED", "2026-01-12"),
            (id_map["Amit"], 799, "PAID", "2026-01-12"),
            (id_map["Pranjali"], 1500, "PENDING", "2026-01-13"),
            (id_map["Rahul"], 1800, "PAID", "2026-01-13"),
        ]
        cur.executemany(
            "INSERT INTO orders (user_id, amount, status, created_at) VALUES (?, ?, ?, ?)",
            orders,
        )

        conn.commit()


def init_db():
    # Create the database on first run.
    if not os.path.exists(DB_FILE):
        reset_db()


def run_query(query):
    with get_connection() as conn:
        return pd.read_sql_query(query, conn)


def get_schema_summary():
    with get_connection() as conn:
        summary = {}
        for table in ["users", "orders"]:
            # PRAGMA gives a quick, beginner-friendly schema snapshot.
            df = pd.read_sql_query(f"PRAGMA table_info({table});", conn)
            summary[table] = df[["name", "type"]]
        return summary


def main():
    st.set_page_config(page_title="SQL Practice App (Beginner) — SQLite", layout="wide")
    st.title("🧠 SQL Practice App (Beginner) — SQLite")
    st.markdown(
        """
        <style>
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            h1 {
                font-size: 1.6rem;
                line-height: 1.2;
            }
            [data-testid="stHorizontalBlock"] {
                flex-direction: column;
                gap: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    init_db()

    if "sql_input" not in st.session_state:
        st.session_state.sql_input = ""
    if "example_choice" not in st.session_state:
        st.session_state.example_choice = "Select an example"

    def load_example():
        choice = st.session_state.example_choice
        if choice in EXAMPLES:
            st.session_state.sql_input = EXAMPLES[choice]

    left, right = st.columns([1, 1])

    with left:
        st.subheader("Query Runner")
        st.selectbox(
            "Load example",
            options=["Select an example"] + list(EXAMPLES.keys()),
            key="example_choice",
            on_change=load_example,
        )
        st.text_area("SQL input", height=220, key="sql_input")

        run_clicked = st.button("Run Query", type="primary")
        reset_clicked = st.button("Reset Sample Database")

        if reset_clicked:
            reset_db()
            st.success("Database reset done ✅")

        if run_clicked:
            query = st.session_state.sql_input.strip()
            if not query:
                st.warning("Please enter a SQL query.")
            else:
                query = query.rstrip(";").strip()
                # Safety: only allow SELECT queries in this practice app.
                if not query.lower().startswith("select"):
                    st.error(
                        "Only SELECT queries are allowed in this beginner app (for safety)."
                    )
                else:
                    try:
                        df = run_query(query)
                        st.dataframe(df, use_container_width=True)
                        st.success(f"Returned {len(df)} rows ✅")
                    except Exception as exc:
                        st.error(str(exc))

    with right:
        st.subheader("Exercises (try these)")
        st.markdown("\n".join([f"{i + 1}) {text}" for i, text in enumerate(EXERCISES)]))

        st.subheader("Table Info")
        schema = get_schema_summary()
        for table, df in schema.items():
            st.markdown(f"**{table}**")
            st.dataframe(df, use_container_width=True)

    st.caption("powered by Adarsh Dessai the Software Architect")


if __name__ == "__main__":
    main()
