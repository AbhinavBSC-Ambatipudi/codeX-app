import streamlit as st
from config.database import authenticate_user
import time
import json
import os

def save_session_state():
    """Save session state to a file"""
    session_data = {
        'authenticated': st.session_state.authenticated,
        'username': st.session_state.username,
        'current_page': st.session_state.current_page,
        'last_activity': st.session_state.last_activity,
        'remember_me': st.session_state.get('remember_me', False)
    }
    with open('session_state.json', 'w') as f:
        json.dump(session_data, f)

def load_session_state():
    """Load session state from file"""
    if os.path.exists('session_state.json'):
        with open('session_state.json', 'r') as f:
            session_data = json.load(f)
            if session_data.get('remember_me', False):
                # Only restore if remember me was checked
                st.session_state.authenticated = session_data['authenticated']
                st.session_state.username = session_data['username']
                st.session_state.current_page = session_data['current_page']
                st.session_state.last_activity = session_data['last_activity']
                st.session_state.remember_me = session_data['remember_me']

def login_page():
    # Try to load saved session state
    if 'remember_me' not in st.session_state:
        load_session_state()
    
    # Custom CSS for login page
    st.markdown("""
    <style>
    .login-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #2D2E3A;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        border-top: 2px solid #4EFB79;
    }
    
    .login-title {
        color: #4EFB79 !important;
        text-align: center;
        margin-bottom: 1.5rem !important;
        font-size: 1.8rem !important;
    }
    
    .login-subtitle {
        color: #E1E1E6 !important;
        text-align: center;
        margin-bottom: 1.5rem !important;
    }
    
    .login-buttons {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="login-title">AI Code Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="login-subtitle">Login to your account</h3>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        remember_me = st.checkbox("Remember me")
        submit = st.form_submit_button("Login")
        
        if submit:
            if authenticate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.current_page = "home"
                st.session_state.username = username
                st.session_state.last_activity = time.time()
                st.session_state.remember_me = remember_me
                
                # Save session state if remember me is checked
                if remember_me:
                    save_session_state()
                
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    st.markdown('<div class="login-buttons">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Account"):
            st.session_state.current_page = "signup"
            st.rerun()
    with col2:
        if st.button("Forgot Password"):
            st.session_state.current_page = "forgot_password"
            st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True) 