import streamlit as st

from src.functions.functions import save_system_state
from src.user_access.signup import signup
from src.user_access.login import login

# Function to handle user entry (log in/sign-up selection)
def user_entry():
    # Create two columns for Login and Signup buttons
    col_login, col_signup = st.columns(2)
    # "Log In" button
    with col_login:
        # If clicked, update session_state.active_entry to "Login"
        if st.button("Log In", type="primary", use_container_width=True):
            st.session_state.active_entry = "Login"
    # "Sign-Up" button
    with col_signup:
        # If clicked, update session_state.active_entry to "Signup"
        if st.button("Sign-Up", use_container_width=True):
            st.session_state.active_entry = "Signup"

    save_system_state()

    # Conditional logic to display Log in/Sign-up page based on session_state.active_entry
    if st.session_state.active_entry == "Login":
        # Call the login function
        login()
    elif st.session_state.active_entry == "Signup":
        # Call the signup function
        signup()