import pandas as pd
import os
import bcrypt
from pathlib import Path
from datetime import datetime
import sqlite3

# Create data directory if it doesn't exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# File paths
USERS_FILE = DATA_DIR / "users.csv"
USER_CODE_FILE = DATA_DIR / "user_code.csv"
CHAT_HISTORY_FILE = DATA_DIR / "chat_history.csv"

def get_db_connection():
    conn = sqlite3.connect('code_snippets.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database files if they don't exist"""
    if not USERS_FILE.exists():
        pd.DataFrame(columns=["username", "email", "password", "created_at"]).to_csv(USERS_FILE, index=False)
    if not USER_CODE_FILE.exists():
        pd.DataFrame(columns=["username", "code", "created_at"]).to_csv(USER_CODE_FILE, index=False)
    if not CHAT_HISTORY_FILE.exists():
        pd.DataFrame(columns=["username", "role", "content", "created_at"]).to_csv(CHAT_HISTORY_FILE, index=False)

    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS code_snippets
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         username TEXT NOT NULL,
         code TEXT NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

def get_users():
    """Get all users from the CSV file"""
    if USERS_FILE.exists():
        return pd.read_csv(USERS_FILE)
    return pd.DataFrame(columns=["username", "email", "password", "created_at"])

def get_user_code():
    """Get all user code from the CSV file"""
    if USER_CODE_FILE.exists():
        return pd.read_csv(USER_CODE_FILE)
    return pd.DataFrame(columns=["username", "code", "created_at"])

def save_users(users_df):
    """Save users DataFrame to CSV"""
    users_df.to_csv(USERS_FILE, index=False)

def save_user_code(code_df):
    """Save user code DataFrame to CSV"""
    code_df.to_csv(USER_CODE_FILE, index=False)

def register_user(username, email, password):
    """Register a new user"""
    users_df = get_users()
    
    # Check if username or email already exists
    if username in users_df["username"].values or email in users_df["email"].values:
        return False
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Add new user
    new_user = pd.DataFrame([{
        "username": username,
        "email": email,
        "password": hashed_password.decode('utf-8'),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    save_users(users_df)
    return True

def authenticate_user(username, password):
    """Authenticate a user"""
    users_df = get_users()
    user = users_df[users_df["username"] == username]
    
    if not user.empty:
        stored_password = user.iloc[0]["password"]
        return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
    return False

def reset_password(username, email, new_password):
    """Reset user password"""
    users_df = get_users()
    user = users_df[(users_df["username"] == username) & (users_df["email"] == email)]
    
    if not user.empty:
        # Hash new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        # Update password
        users_df.loc[users_df["username"] == username, "password"] = hashed_password.decode('utf-8')
        save_users(users_df)
        return True
    return False

def save_user_code_snippet(username, code):
    conn = get_db_connection()
    conn.execute('INSERT INTO code_snippets (username, code) VALUES (?, ?)',
                (username, code))
    conn.commit()
    conn.close()

def get_user_code_snippets(username):
    conn = get_db_connection()
    snippets = pd.read_sql_query(
        'SELECT * FROM code_snippets WHERE username = ? ORDER BY created_at DESC',
        conn,
        params=(username,)
    )
    conn.close()
    return snippets

def delete_user_code_snippet(snippet_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM code_snippets WHERE id = ?', (snippet_id,))
    conn.commit()
    conn.close()

def get_chat_history(username):
    """Get chat history for a specific user"""
    if CHAT_HISTORY_FILE.exists():
        chat_df = pd.read_csv(CHAT_HISTORY_FILE)
        user_chat = chat_df[chat_df["username"] == username]
        return user_chat.sort_values("created_at")
    return pd.DataFrame(columns=["username", "role", "content", "created_at"])

def save_chat_message(username, role, content):
    """Save a chat message"""
    chat_df = pd.read_csv(CHAT_HISTORY_FILE) if CHAT_HISTORY_FILE.exists() else pd.DataFrame(columns=["username", "role", "content", "created_at"])
    
    new_message = pd.DataFrame([{
        "username": username,
        "role": role,
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    chat_df = pd.concat([chat_df, new_message], ignore_index=True)
    chat_df.to_csv(CHAT_HISTORY_FILE, index=False)

def clear_chat_history(username):
    """Clear chat history for a specific user"""
    if CHAT_HISTORY_FILE.exists():
        chat_df = pd.read_csv(CHAT_HISTORY_FILE)
        # Keep only messages from other users
        chat_df = chat_df[chat_df["username"] != username]
        chat_df.to_csv(CHAT_HISTORY_FILE, index=False)
        return True
    return False

# Initialize the database when this module is imported
init_db() 