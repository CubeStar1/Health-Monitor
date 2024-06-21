import streamlit as st
from supabase import create_client
st.set_page_config(layout="wide")
from supabase import create_client

SUPABASE_URL = "https://khpbpwchudsamfigczsj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtocGJwd2NodWRzYW1maWdjenNqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg5NTU3MDYsImV4cCI6MjAzNDUzMTcwNn0.jsP_CmBT8gDDulvcsMxp6U7oK8HxBL9QAm5y4gTsIHk"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



def authenticated_menu():
    st.sidebar.page_link("pages/sensor_dashboard.py", label="Sensor Dashboard")
    st.sidebar.page_link("pages/health_report.py", label="Health Report Generator")
    # st.sidebar.page_link("app.py", label="Log out")

def unauthenticated_menu():
    st.sidebar.page_link("app.py", label="Log in")

def menu():
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
    else:
        authenticated_menu()

# Example login function (replace with actual logic)
def login(username, password):
    if username == "user" and password == "pass":
        st.session_state.role = "user"
        st.experimental_rerun()
    else:
        st.error("Invalid credentials")

# Logout function
def logout():
    if "role" in st.session_state:
        del st.session_state["role"]
    st.success("Logged out successfully")
    st.experimental_rerun()

# UI for login if user is not logged in
if "role" not in st.session_state or st.session_state.role is None:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Log in"):
        login(username, password)
else:
    st.switch_page("pages/sensor_dashboard.py")
    # st.title("Welcome to the Dashboard")
    # st.success("You are logged in.")
    # if st.button("Log out"):
    #     logout()
    # menu()
