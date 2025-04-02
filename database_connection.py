import duckdb
from datetime import datetime

conn = duckdb.connect("database/bank.duckdb")

conn.execute("""
    CREATE TABLE IF NOT EXISTS user (
        account_id STRING,
        username STRING,
        password STRING,
        account_balance DOUBLE,
        account_creation_timestamp TIMESTAMP
    );
""")

conn.execute("""
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

# account_creation_timestamp = datetime.now()

# # conn.execute(f"""
# #     INSERT INTO user (account_id, username, password, account_balance, account_creation_timestamp)
# #     VALUES ('ID_00001', 'addison', '123', 10000, CAST('{account_creation_timestamp}' AS TIMESTAMP));
# # """)

# res = conn.execute("SELECT * FROM transaction").fetchone()

# # for row in res:
# #     print(row)

# print(True) if res else print (False)