import streamlit as st
from config.database import reset_password

def forgot_password_page():
    st.title("Reset Password")
    
    with st.form("forgot_password_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        submit = st.form_submit_button("Reset Password")
        
        if submit:
            if new_password != confirm_password:
                st.error("Passwords do not match")
            elif not username or not email or not new_password:
                st.error("Please fill in all fields")
            else:
                if reset_password(username, email, new_password):
                    st.success("Password reset successfully! Please login with your new password.")
                    st.session_state.current_page = "login"
                    st.rerun()
                else:
                    st.error("Invalid username or email")
    
    if st.button("Back to Login"):
        st.session_state.current_page = "login"
        st.rerun() 