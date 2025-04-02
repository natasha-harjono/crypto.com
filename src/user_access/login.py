import streamlit as st

from src.functions.functions import save_system_state, user_exist, get_user_details, update_last_active
from src.user_access.password import hash_password

# Function to handle user login
def login():
    # INITIALIZE SESSION STATE
    # "user": Stores logged in user details.
    # "user_id" (str), "username" (str), "account_balance" (float)
    if "user" not in st.session_state:
        st.session_state.user = {"account_id": None, "username": None, "account_balance": None}

    # Display subheader for log in section
    st.subheader("LOG IN")

    # Required input fields to log in
    username = st.text_input("Username:", placeholder="Enter your username", value='', on_change=update_last_active())
    password = st.text_input("Password:", placeholder="Enter your password", value='', type="password", on_change=update_last_active())

    # "Log In" button 
    if st.button("Log In", on_click=update_last_active()):
        # Check if both fields are populated
        if username and password:
            username = username.lower()
            # Check if username exists in the user table
            if user_exist(username):
                # Hash the entered password
                hashed_password = hash_password(password)
                # Retrive the password (hashed) for the entered username
                user_details = get_user_details(username)

                # Check if password matches
                if hashed_password == user_details[0][1]:
                    # Log in successfull
                    st.success(f"Welcome, {username}!")
                    # Store logged in user details in session state
                    account_id = user_details[0][0]
                    account_balance = user_details[0][2]
                    st.session_state.user = {"account_id": account_id, "username": username, "account_balance": account_balance}
                    # Update session_state.login to True
                    st.session_state.login = True
                    save_system_state()
                    st.rerun()
                else:
                    # Print error messege if password does not match
                    st.error("Incorrect password. Please try again.")
            else:
                # Print error messege if username does not exist in user table
                st.error("Username not found. Check your entry, it's case-sensitive. New here? Sign up to get started!")
        else:
            # Print error messege if username and/or password is blank
            st.error("Username or password cannot be blank. Please fill in both fields to continue.")