# Crypto.com Take-Home Test Submission  
## **Python Data Engineer Role**  

### **Overview**  
This web application provides a simple banking system that enables users to create accounts and perform transactions.

---

### **Features**  

#### 1. **User Sign-Up**  
- New users can register by providing their username, password, and a starting balance.  
- Passwords are encrypted before storage to ensure security.  

#### 2. **User Login**  
- Registered users can log in using their credentials to access their accounts.  

#### 3. **Transactions**  
- Users can perform various transactions, including:  
  - **Deposit**: Add funds to their account.  
  - **Withdraw**: Deduct funds from their account.  
  - **Transfer**: Transfer funds to other accounts within the system.

---

### **Database**  
The application leverages **DuckDB** for efficient and lightweight data management. It includes the following tables:  
1. **User Table**:  
   - Stores user-related data such as `account_id`, `username`, `password`, `account_balance`, and `account_creation_timestamp`.  
2. **Transactions Table**:  
   - Captures transaction details including `transaction_id`, `account_id`, `transaction_type`, `credit_debit`, `transaction_timestamp`, `sender_username`, `recepient_username`, `previous_balance`, `transaction_amount`, and `updated_balance`.

---

### **How to Access the App**

#### **1. Locally**
To run the app locally:
```bash
git clone https://github.com/natasha-harjono/crypto.com.git
cd crypto.com
pip install -r requirements.txt
streamlit run app.py
```

#### **2. Access the Deployed App**
To access the live deployment, visit the following link: https://cryptodotcom-submission.streamlit.app/





   
