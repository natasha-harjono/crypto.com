import hashlib

# Function to hash passwords
def hash_password(password):
    # Returns the hashed value of the input password
    return hashlib.sha256(password.encode()).hexdigest()