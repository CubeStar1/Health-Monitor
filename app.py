import streamlit as st
import sqlite3
import hashlib
import os


def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                 (id INTEGER PRIMARY KEY, user_id INTEGER, 
                  heart_rate REAL, temperature REAL, ecg REAL, spo2 REAL, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()




def register_user(username, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()



def authenticate_user(username, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE username=? AND password=?", (username, hashed_password))
    result = c.fetchone()
    conn.close()
    return result



def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def update_username(user_id, new_username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def update_password(user_id, new_password):
    hashed_password = hash_password(new_password)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))
    conn.commit()
    conn.close()
    return True

def delete_account(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DELETE FROM sensor_data WHERE user_id = ?", (user_id,))
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True
init_db()


is_admin_user = lambda username: username == "admin"

st.set_page_config(page_title="Health Monitor", page_icon="🩺", layout="centered")

if "role" not in st.session_state or st.session_state.role is None:
    with st.container(border=True):

        header_html = """
                <style>
                .gradient-container {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    margin: 0rem 0rem 1rem 0rem;
                    padding: 20px;
                    border-radius: 10px;
                    background: linear-gradient(45deg, #43cea2, #185a9d);
                    color: white;
                    text-align: center;
                    box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
                }

                .gradient-text {
                    font-size: 2.5em;
                    font-weight: bold;
                }

                .gradient-subtext {
                    font-size: 1.2em;
                    margin-top: 10px;
                }
                </style>
                <div class="gradient-container">
                    <div class="gradient-text">Health Monitor</div>
                    <div class="gradient-subtext">Analyze and visualize your health data with ease</div>
                </div>

                """


        st.markdown(header_html, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            with st.form(key="login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button("Log in")

                if submit_button:
                    result = authenticate_user(username, password)
                    if result:
                        st.session_state.role = "user"
                        st.session_state.username = result[1]
                        st.session_state.user_id = result[0]
                        if is_admin_user(username):
                            st.session_state.role = "admin"
                        st.success("Logged in successfully!")
                        st.experimental_rerun()
                    else:
                        st.error("Invalid credentials")

        with tab2:
            with st.form(key="signup_form"):
                new_username = st.text_input("Choose a Username")
                new_password = st.text_input("Choose a Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                signup_button = st.form_submit_button("Sign Up")

                if signup_button:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif register_user(new_username, new_password):
                        st.success("Account created successfully! Please log in.")
                    else:
                        st.error("Username already exists")

else:
    st.title(f"Welcome, {st.session_state.username}!")
    if st.button("Log out"):
        logout()
        st.experimental_rerun()


    st.switch_page("pages/sensor_dashboard.py")

