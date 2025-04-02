import streamlit as st
import pandas as pd
import json
import database_connection
from datetime import datetime

system_state_path = "system/system_state.csv"

# Function to store system path in csv
def save_system_state():
    state = {key: (json.dumps(value) if isinstance(value, (dict, list)) else value) for key, value in st.session_state.items()}
    df = pd.DataFrame([state])  # Convert session state to DataFrame
    #df = pd.DataFrame([st.session_state])
    df.to_csv(system_state_path, index=False)

# Function to load system state
def load_system_state():
    try:
        # Load CSV into a DataFrame
        df = pd.read_csv(system_state_path)
        # Convert DataFrame to dictionary and update session state
        last_active_value = dict(df.iloc[0].items()).get("last_active", "Column not found")
        delta = datetime.now() - pd.to_datetime(last_active_value)

        if delta.total_seconds() < 600.00 and st.session_state.login == True:
            #st.header(delta.total_seconds())
            for key, value in df.iloc[0].items():
                try:
                    st.session_state[key] = json.loads(value)  # Attempt to decode JSON
                except (TypeError, json.JSONDecodeError):
                    st.session_state[key] = value
    except:
        pass

# Function to update user's last active time
def update_last_active():
    st.session_state.last_active = datetime.now() 

def initialize_database():
    database_connection.conn.execute("""
        CREATE TABLE IF NOT EXISTS user (
            account_id STRING,
            username STRING,
            password STRING,
            account_balance DOUBLE,
            account_creation_timestamp TIMESTAMP
        );
    """)

    database_connection.conn.execute("""
        CREATE TABLE IF NOT EXISTS transaction (
            transaction_id STRING,
            account_id STRING,
            transaction_type STRING,
            credit_debit STRING,
            transaction_timestamp TIMESTAMP,
            sender_username STRING,
            recepient_username STRING,
            account_creation_timestamp TIMESTAMP,
            previous_balance DOUBLE,
            transaction_amount DOUBLE,
            updated_balance DOUBLE
        );
    """)    

# Function to check if a user esixt in user tables
def user_exist(username):
    result = database_connection.conn.execute(f"SELECT 1 FROM user WHERE username == '{username}'").fetchone()
    return True if result else False

# Function to get a user detail
def get_user_details(username):
    result = database_connection.conn.execute(f"SELECT account_id, password, account_balance FROM user WHERE username == '{username}'").fetchall()
    return result

# Function to add a new user to the user table
def add_user(account_id, username, password, account_balance, account_creation_timestamp):
    database_connection.conn.execute(f"""
        INSERT INTO user (account_id, username, password, account_balance, account_creation_timestamp)
        VALUES ('{account_id}', '{username}', '{password}', {account_balance}, CAST('{account_creation_timestamp}' AS TIMESTAMP));
    """)

# Function to get the row number of a table
def get_row_count(table_name):
    result = database_connection.conn.execute(f"SELECT COUNT(*) FROM {table_name};").fetchone()
    return int(result[0])

# Function to add a new transaction to the transaction table
def add_transaction(transaction_id, account_id, transaction_type, credit_debit, transaction_timestamp, sender_username, recepient_username, previous_balance, transaction_amount, updated_balance):
    database_connection.conn.execute(f"""
        INSERT INTO transaction (transaction_id, account_id, transaction_type, credit_debit, transaction_timestamp, sender_username, recepient_username, previous_balance, transaction_amount, updated_balance)
        VALUES ('{transaction_id}', '{account_id}', '{transaction_type}', '{credit_debit}', CAST('{transaction_timestamp}' AS TIMESTAMP), '{sender_username}', '{recepient_username}', {previous_balance}, {transaction_amount}, {updated_balance});
    """)

#Function to update the user's account balance in user table
def update_user_account_balance(username, new_balance):
    database_connection.conn.execute(f"UPDATE user SET account_balance = {new_balance} WHERE username = '{username}';")

# Function to logout of the account
def logout():
    st.session_state.login = False
    if "active_action" in st.session_state:
        del st.session_state.active_action
    if "active_ind" in st.session_state:
        del st.session_state.active_ind
    del st.session_state.user
    del st.session_state.last_active
    save_system_state()
    st.rerun()