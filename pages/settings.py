import streamlit as st
import sqlite3

# Import the functions we just created
from app import update_username, update_password, delete_account, logout
from  utils import menu_with_redirect
from utils import menu_with_redirect




def settings_page():
    if "user_id" not in st.session_state:
        st.error("Please log in to access the settings.")
        if st.button("Go to Login"):
            st.switch_page("app.py")
        return

    st.title("Account Settings")

    with st.container(border=True):
        st.subheader("Change Username")
        new_username = st.text_input("New Username")
        if st.button("Update Username"):
            if update_username(st.session_state.user_id, new_username):
                st.session_state.username = new_username
                st.success("Username updated successfully!")
            else:
                st.error("Username already exists or an error occurred.")

    with st.container(border=True):
        st.subheader("Change Password")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        if st.button("Update Password"):
            if new_password != confirm_password:
                st.error("New passwords do not match.")
            elif update_password(st.session_state.user_id, new_password):
                st.success("Password updated successfully!")
            else:
                st.error("An error occurred while updating the password.")

    with st.container(border=True):
        st.subheader("Delete Account")
        st.warning("This action cannot be undone. All your data will be permanently deleted.")
        delete_confirmation = st.text_input("Type 'DELETE' to confirm account deletion")
        if st.button("Delete Account"):
            if delete_confirmation == "DELETE":
                if delete_account(st.session_state.user_id):
                    st.toast("Your account has been deleted.")
                    logout()
                    st.switch_page("app.py")
                else:
                    st.error("An error occurred while deleting your account.")
            else:
                st.error("Please type 'DELETE' to confirm account deletion.")


menu_with_redirect()
settings_page()
