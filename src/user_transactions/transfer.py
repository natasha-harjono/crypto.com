import streamlit as st
from datetime import datetime
import pandas as pd

from src.functions.functions import add_transaction, update_user_account_balance, save_system_state, user_exist, get_user_details, get_row_count, update_last_active

def transfer(account_id, username, account_balance):
    # Display subheader for Transfer section
    st.markdown("### Transfer Funds")

    # Required input fields to make a transfer
    transfer_to = st.text_input("Recipient Username:", on_change=update_last_active())
    transfer_amount = st.number_input("Enter transfer amount:", min_value=0.0, step=0.01, on_change=update_last_active())

    # Create three columns for "Confirm Deposit" and "Close" button, middle column is empty for display purpose
    col_confirm, col_space, col_close = st.columns([2.35, 7.2, 0.7])
    # "Close" button
    with col_close:
        # If clicked, reset the session_state.active_action to None
        # This will close the Deposit popup/page
        if st.button("Close", type="tertiary", on_click=update_last_active()):
            st.session_state.active_action = None  # Reset the active popover
            save_system_state()
            st.rerun()  # Force rerun to immediately hide the popover
    # "Confirm Transfer" button
    with col_confirm:
        # If clicked, transfer the entered amount
        if st.button("Confirm Transfer", on_click=update_last_active()):
            # Check if the recipient is not the user
            transfer_to = transfer_to.lower()
            username = username.lower()
            if transfer_to != username:
                #Checked if the recipient has an account
                if user_exist(transfer_to):
                    # Check if there is enough balance to transfer
                    if transfer_amount <= account_balance:
                        # Check if transfer_amount is more than 0
                        if transfer_amount > 0:
                            # Generate transaction_id
                            transaction_id = datetime.now().strftime('%Y%m%d') + str(get_row_count("transaction")+1).zfill(5)
                            # Calculate sender new account balance after subsracting the transfer amount
                            new_balance = account_balance - transfer_amount
                            # Retrive recipient account account_id and balance
                            recipient_details = get_user_details(transfer_to)
                            recipient_account_id = recipient_details[0][0]
                            recipient_account_balance = recipient_details[0][2]
                            # Calculate recipient new account balance after adding the transfer amount
                            recipient_new_balance = recipient_account_balance + transfer_amount

                            # Create a new transaction record in user transaction for both sender and recepient
                            add_transaction(transaction_id + '-D', account_id, "TRANSFER", "D", datetime.now(), username, transfer_to.lower(), account_balance, -transfer_amount, new_balance)
                            add_transaction(transaction_id + '-C', recipient_account_id, "TRANSFER", "C", datetime.now(), username, transfer_to.lower(), recipient_account_balance, transfer_amount, recipient_new_balance)
                            # Update the acccount balance in user table for both sender and recepient
                            update_user_account_balance(username, new_balance)
                            update_user_account_balance(transfer_to.lower(), recipient_new_balance)
                            # Update the session_state.user["balance"] to the new balance
                            st.session_state.user["account_balance"] = new_balance
                            
                            # Update st.session_state.active_ind to return success
                            message = f"Successfully transferred HKD {transfer_amount:,.2f} to {transfer_to}!"
                            st.session_state.active_ind = {"success": True, "message": message}
                            st.balloons()

            # Update st.session_state.active_ind to return fail and return error message
                        else:
                            message = "Transfer amount must be greater then 0. Please enter a valid value."
                            st.session_state.active_ind = {"success": False, "message": message}
                    else:
                        message = "Insufficient balance. Please check your account and try again."
                        st.session_state.active_ind = {"success": False, "message": message}
                else:
                    message = f"Recipient {transfer_to} not found. Please double-check the username and try again."
                    st.session_state.active_ind = {"success": False, "message": message}
            else:
                message = "You can't transfer funds to yourself. Please select a different recipient."
                st.session_state.active_ind = {"success": False, "message": message}
            
    save_system_state()