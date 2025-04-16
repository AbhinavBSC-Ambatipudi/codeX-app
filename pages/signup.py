import streamlit as st
from config.database import register_user

def signup_page():
    st.title("Create New Account")
    
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if password != confirm_password:
                st.error("Passwords do not match")
            elif not username or not email or not password:
                st.error("Please fill in all fields")
            else:
                if register_user(username, email, password):
                    st.success("Account created successfully! Please login.")
                    st.session_state.current_page = "login"
                    st.rerun()
                else:
                    st.error("Username or email already exists")
    
    if st.button("Back to Login"):
        st.session_state.current_page = "login"
        st.rerun() 