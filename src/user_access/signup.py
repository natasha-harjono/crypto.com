import streamlit as st
from datetime import datetime
import database_connection

from src.functions.functions import user_exist, add_user, get_row_count, update_last_active, add_transaction
from src.user_access.login import hash_password

# Function to handle user sign-up
def signup():
    # Display subheader for sign-up section
    st.subheader("SIGN-UP")

    # Required input fields to sign up
    new_username = st.text_input("Username:", placeholder="Enter your username", value=None, on_change=update_last_active())
    new_password = st.text_input("Password:", placeholder="Enter your password", value=None, type="password", on_change=update_last_active()) # hidden for security
    new_balance = st.number_input("Account Starting Balance:", value=None, min_value=0, placeholder="Enter your account starting balance", on_change=update_last_active())

    # "Sign-Up" button
    if st.button("Sign-Up", on_click=update_last_active()):
        # Check if both fields are populated
        if new_username and new_password and new_balance != None:
            new_username = new_username.lower()
            # Check the entered starting balance is more than 0
            if new_balance > 0:
                # Check if username exists in the user table
                if not user_exist(new_username):
                    # Generate transaction_id
                    transaction_id = datetime.now().strftime('%Y%m%d') + str(get_row_count("transaction")+1).zfill(5)
                    # Get the current date and time for account_creation_timestamp
                    account_creation_timestamp = datetime.now()
                    # Generate unique acccount_id
                    new_account_id = "ID_" + str(get_row_count("user")+1).zfill(5)
                    # Hash entered password
                    hashed_password = hash_password(new_password)

                    # Create a new user record in user table
                    add_user(new_account_id, new_username, hashed_password, new_balance, account_creation_timestamp)
                    # Create a new transaction record in user transaction for the starting balance
                    add_transaction(transaction_id, new_account_id, "DEPOSIT", "C", datetime.now(), '', new_username, 0, new_balance, new_balance)
                    # Display success message after account creation
                    st.success("Account created successfully! You can now log in to access your account.")
                else:
                    # Print warning messege to notify user
                    st.warning("Username already exists. Please try a different one.")
            else:
                # Print error messege if balance < 0
                st.error("Account starting balance should be more than 0.")
        else:
            # Print error messege if username and/or password is blank
            st.error("Username, Password, and Starting Balance cannot be blank. Please fill in both fields to continue.")