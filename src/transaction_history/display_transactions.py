import streamlit as st
import pandas as pd
import database_connection

# Function to get user transaction
def get_user_transactions(account_id):
    # Retrieve user's past transactions
    user_transaction_df = database_connection.conn.execute(f"SELECT * FROM transaction WHERE account_id == '{account_id}';").fetchdf()
    
    # Check if user has past transactions
    if user_transaction_df.empty:
        st.info("No transactions found.")
    else:
        # Function to generate transaction description
        def generate_description(row):
            if row["transaction_type"].lower() == "deposit":
                return "DEPOSIT"
            elif row["transaction_type"].lower() == "withdraw":
                return "WITHDRAW"
            elif row["transaction_type"].lower() == "transfer" and row["credit_debit"].lower() == "c":
                return f"TRANSFER IN FROM {row["sender_username"].upper()}"
            elif row["transaction_type"].lower() == "transfer" and row["credit_debit"].lower() == "d":
                return f"TRANSFER OUT TO {row["recepient_username"].upper()}"
            else:
                return "UNKNOWN"
        
        # Function to format transaction amount
        def format_to_hkd(value):
            if value < 0:
                return f"- HKD {abs(value):,.2f}"  # Format negative numbers
            else:
                return f"HKD {value:,.2f}"  # Format positive numbers

        # Preprocess the user_transaction_df
        user_transaction_df["DESCRIPTION"] = user_transaction_df.apply(generate_description, axis=1)
        user_transaction_df["TRANSACTION AMOUNT"] = user_transaction_df.apply(lambda row: abs(row["transaction_amount"]) if row["credit_debit"] == "C" else -abs(row["transaction_amount"]), axis=1)
        user_transaction_df["TRANSACTION AMOUNT"] = user_transaction_df["TRANSACTION AMOUNT"].apply(format_to_hkd)
        user_transaction_df["TRANSACTION DATE & TIME"] = pd.to_datetime(user_transaction_df["transaction_timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        user_transaction_df = user_transaction_df[["TRANSACTION DATE & TIME", "DESCRIPTION", "TRANSACTION AMOUNT"]]
        user_transaction_df = user_transaction_df.sort_values(by="TRANSACTION DATE & TIME", ascending=False)

        # Add style to table
        def highlight_negative_amounts(row):
            if float(row["TRANSACTION AMOUNT"].replace(" ", "").replace("HKD", "").replace(",", "")) < 0:
                return ["background-color: maroon"] * len(row)  # Highlight in light red
            else:
                return ["background-color: darkslategrey"] * len(row)  # No highlight

        # Apply the style function to the DataFrame
        styled_df = (
            user_transaction_df.style
                .apply(highlight_negative_amounts, axis=1))  # Highlight rows
   
        # Display the transaction history as a table
        st.dataframe(styled_df, hide_index = True, use_container_width=True, height = 450)
