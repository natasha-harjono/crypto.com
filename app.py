import streamlit as st
import pandas as pd
from datetime import datetime

from src.functions.functions import save_system_state, load_system_state, logout, initialize_database
from src.user_access.entry import user_entry
from src.user_transactions.transactions import user_transactions
from src.transaction_history.display_transactions import get_user_transactions

# Load database
#initialize_database()

def main():
    # Load system state from csv
    load_system_state()
    # Initialize/load database

    # INITIALIZE SESSION STATE
    # login_ind (boolean): True if the user is logged in, False otherwise.
    if "login" not in st.session_state:
        st.session_state.login = False

    if "last_active" not in st.session_state:
        st.session_state.last_active = datetime.now()

    # active_entry (str): Tracks current active popup/page ("Login"/"Signup"). Default to "Login".
    if "active_entry" not in st.session_state:
        st.session_state.active_entry = "Login"


    # HANDLE USER LOG IN AND/OR SIGN-UP
    if not st.session_state.login:
        # Display "Welcome Back!" header
        st.markdown("<h1 style='text-align: center;'>Welcome Back!</h1>", unsafe_allow_html=True)
        # Call the user_entry functsion
        with st.container(border=True):
            user_entry()

    save_system_state()

    # MAIN WEB APP AFTER LOGGING IN
    if st.session_state.login:
        # Logic to log user out after 10 minutes of inactivity
        delta = datetime.now() - pd.to_datetime(st.session_state.last_active)
        if delta.total_seconds() > 600.00:
            logout()

        # Get logged in user"s account_id, username, and balance
        account_id = st.session_state.user["account_id"]
        username = st.session_state.user["username"].capitalize()
        account_balance = st.session_state.user["account_balance"]
        formatted_balance = f"HKD {account_balance:,.2f}"


        # DEFINE HEADER AND LOG OUT BUTTON
        col_header1, colheader2 = st.columns([14.3,2])
        # Display "Hi, {username}!" header
        with col_header1:
            st.markdown(f"""
                <h1 style="font-size:55px; font-style:italic; color: white; text-align: left; margin-bottom: 20px;">
                    Hi, {username}!
                </h1>
            """, unsafe_allow_html=True)
        # Log out button
        # If clicked, update session_state.login["login_ind"] to False, this will allow users to go back to log in/ sign-up screen
        with colheader2:
            if st.button("Log Out"):
                logout()


        # DISPLAY ACCOUNT BALANCE
        with st.container(border=True):
            space1, metric, space2 = st.columns([0.8, 2, 0.5])
            with metric:
                st.metric(label="Balance", value=f"{formatted_balance}")


        # HANDLE USER ACTIONS/TRANSACTIONS (DEPOSIT, WITHDRAW, AND TRANSFER)
        # Display "Manage Your Funds" subheader
        st.markdown("""
            <h3 style="font-size:35px;color: white; text-align: center; margin-top: 20px; margin-bottom: 8px;">Manage Your Funds</h3>
        """, unsafe_allow_html=True)
        # Call the user_transactions function
        user_transactions(account_id, username, account_balance)


        # DISPLAY USER'S TRANSACTION HISTORY
        # Display "Transaction History" subheader
        st.markdown("""
            <h3 style="font-size:35px;color: white; text-align: center; margin-top: 20px;">Transaction History</h3>
        """, unsafe_allow_html=True)
        # Call the get_user_transactions function to display pas transaction related to user
        get_user_transactions(account_id)


if __name__ == "__main__":
    main()