import streamlit as st


def logout():
    if "role" in st.session_state:
        del st.session_state["role"]
    st.success("Logged out successfully")
    st.experimental_rerun()
def authenticated_menu():
    with st.sidebar:
        with st.container(border=True):
            st.image('idea-lab-round.png')
            st.page_link("pages/sensor_dashboard.py", label="Sensor Dashboard")
            st.page_link("pages/health_report.py", label="Health Report Generator")
            st.page_link("pages/chat.py", label="Chat Dashboard")
            # st.page_link("app.py", label="Log out")
            if st.button("Log out", use_container_width=True):
                logout()
def unauthenticated_menu():

    st.sidebar.page_link("app.py", label="Log in")

def menu():
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
    else:
        authenticated_menu()

def menu_with_redirect():
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    else:
        menu()
