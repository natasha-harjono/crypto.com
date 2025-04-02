import streamlit as st
import pandas as pd
import time

from src.functions.functions import save_system_state, update_last_active
from src.user_transactions.deposit import deposit
from src.user_transactions.withdraw import withdraw
from src.user_transactions.transfer import transfer

def user_transactions(account_id, username, account_balance):
    # INITIALIZE SESSION STATE 
    # active_action (str): Tracks current active transaction popup/page ("Deposit"/"Withdraw"/"Transfer")
    if "active_action" not in st.session_state:
        st.session_state.active_action = None
    # status (1/0): Indicates if the transaction is successfull (True) or not (False)
    # message (str): Return message to be displayed
    if "action_return" not in st.session_state:
        st.session_state.active_ind = {"success": None, "message": None}

    # Create three columns for Deposit, Withdraw, and Transfer buttons
    col_deposit, col_withdraw, col_tranfer = st.columns(3) 
    # Resets session_state.active_ind  for the next transaction
    st.session_state.active_ind = {"success": None, "message": None}
    # "Deposit" button
    with col_deposit:
        # If clicked, update session_state.active_action to Deposit
        if st.button("Deposit", type="primary", use_container_width=True, on_click=update_last_active()):
            st.session_state.active_action = "Deposit"
            #save_system_state()
    # Withdraw" button
    with col_withdraw:
        # If clicked, update session_state.active_action to Withdraw
        if st.button("Withdraw", type="primary", use_container_width=True, on_click=update_last_active()):
            st.session_state.active_action = "Withdraw"
            #save_system_state()
    # "Transfer" button
    with col_tranfer:
        # If clicked, update session_state.active_action to Transfer
        if st.button("Transfer", type="primary", use_container_width=True, on_click=update_last_active()):
            st.session_state.active_action = "Transfer"
            #save_system_state()

    save_system_state()
    
    # Conditional logic to display action's page (deposit/withdraw/transfer) based on session_state.active_action
    if st.session_state.active_action == "Deposit":
        # Call the deposit function
        deposit(account_id, username, account_balance)
    elif st.session_state.active_action == "Withdraw":
        # Call the withdraw function
        withdraw(account_id, username, account_balance)
    elif st.session_state.active_action == "Transfer":
        # Call the transfer function
        transfer(account_id, username, account_balance)

    # Display error/success message
    # Conditional logic to print error or success messege
    if st.session_state.active_ind['success']:
        # Print returned success message
        st.success(st.session_state.active_ind['message'])
        # Reset session_state.active_action
        st.session_state.active_action = None
        # Reset session_state.active_ind for the next transaction
        st.session_state.active_ind = {"success": None, "message": None}
        time.sleep(1.4)
        save_system_state()
        st.rerun()
    elif st.session_state.active_ind['success'] == False:
        # Print returned error message
        st.error(st.session_state.active_ind['message'])

    save_system_state()