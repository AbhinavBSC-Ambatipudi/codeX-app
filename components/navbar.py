import streamlit as st

def navbar():
    # Custom CSS for the navbar
    st.markdown("""
    <style>
    .navbar {
        background-color: #2D2E3A;
        padding: 0.8rem 1rem;
        border-bottom: 1px solid #3A3B45;
        margin-bottom: 1rem;
    }
    .nav-button {
        background-color: #1E1F2C;
        color: #4EFB79;
        border: 1px solid #3A3B45;
        padding: 0.5rem 1rem;
        margin: 0 0.5rem;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .nav-button:hover {
        border-color: #4EFB79;
        background-color: #3A3B45;
    }
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .nav-left {
        display: flex;
        align-items: center;
    }
    .nav-right {
        display: flex;
        align-items: center;
    }
    .logo {
        font-size: 1.5rem;
        font-weight: bold;
        color: #4EFB79;
        margin-right: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Navbar HTML
    st.markdown("""
        <div class="navbar">
            <div class="nav-container">
                <div class="nav-left">
                    <span class="logo">codeX</span>
                </div>
                <div class="nav-right">
    """, unsafe_allow_html=True)

    # Navigation buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("Home", key="nav_home"):
            st.session_state.current_page = "home"
            st.rerun()
    
    with col2:
        if st.button("Code Editor", key="nav_editor"):
            st.session_state.current_page = "code_editor"
            st.rerun()
    
    with col3:
        if st.button("Chat", key="nav_chat"):
            st.session_state.current_page = "chatbot"
            st.rerun()
    
    with col4:
        if st.button("Logout", key="nav_logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.markdown("</div></div></div>", unsafe_allow_html=True) 