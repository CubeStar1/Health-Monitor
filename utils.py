import streamlit as st


def logout():
    if "role" in st.session_state:
        del st.session_state["role"]
    st.success("Logged out successfully")
    st.experimental_rerun()
def authenticated_menu():
    with st.sidebar:
        with st.container(border=True):
            st.image('static/idea-lab-round.png')
            with st.expander("Menu", expanded=True):
                st.page_link("pages/sensor_dashboard.py", label="Health Monitor", icon="🩺")
                st.page_link("pages/health_report.py", label="Health Report", icon="📊")
                st.page_link("pages/chat.py", label="Chat with Health Assistant", icon="💬")
                st.page_link("pages/test.py", label="Data Visualiser", icon="📈")
                st.page_link("pages/about.py", label="About", icon="📖")
                st.page_link("pages/settings.py", label="Account Settings", icon="⚙️")
                st.page_link("pages/admin.py", label="Admin", icon="🔒", disabled="admin" not in st.session_state.role)
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
