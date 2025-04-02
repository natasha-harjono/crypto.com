import streamlit as st
from datetime import datetime

from src.functions.functions import add_transaction, update_user_account_balance, save_system_state, get_row_count, update_last_active

def deposit(account_id, username, account_balance):
    # Display subheader for Deposit section
    st.markdown("### Deposit Funds")
    
    # Input field for deposit amount
    deposit_amount = st.number_input("Enter deposit amount:", value=0.00, min_value=0.0, step=0.01, on_change=update_last_active) 

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
    # "Confirm Deposit" button
    with col_confirm:
        # If clicked, deposit the entered amount
        if st.button("Confirm Deposit", on_click=update_last_active()):
            # Check if deposit_amount is more than 0
            if deposit_amount > 0:
                # Generate transaction_id
                transaction_id = datetime.now().strftime('%Y%m%d') + str(get_row_count("transaction")+1).zfill(5)
                # Calculate new account balance after adding the deposit amount
                new_balance = account_balance + deposit_amount

                # Create a new transaction record in user transaction
                add_transaction(transaction_id, account_id, "DEPOSIT", "C", datetime.now(), '', username, account_balance, deposit_amount, new_balance)
                # Update the acccount balance in user table
                update_user_account_balance(username, new_balance)
                # Update the session_state.user["balance"] to the new balance
                st.session_state.user["account_balance"] = new_balance
                
                # Update st.session_state.active_ind to return success
                message = f"Successfully deposited HKD {deposit_amount:,.2f}!"
                st.session_state.active_ind = {"success": True, "message": message}
                st.balloons()

            # Update st.session_state.active_ind to return fail and return error message
            else:
                message = "Deposit amount must be greater then 0. Please enter a valid value."
                st.session_state.active_ind = {"success": False, "message": message}
        
    save_system_state()
                
