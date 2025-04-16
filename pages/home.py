import streamlit as st
from components.navbar import navbar

def home_page():
    # Add the main navbar
    navbar()
    
    # Custom CSS for home page
    st.markdown("""
    <style>
    .home-container {
        padding: 1.5rem;
    }
    
    .home-title {
        color: #4EFB79 !important;
        margin-bottom: 1rem !important;
        font-size: 3rem !important;
    }
    
    .home-subtitle {
        color: #E1E1E6 !important;
        margin-bottom: 2rem !important;
        font-size: 1.2rem !important;
    }
    
    .feature-card {
        background-color: #2D2E3A;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 2px solid #4EFB79;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        border-left: 4px solid #4EFB79;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        color: #4EFB79;
    }
    
    .feature-title {
        color: #E1E1E6 !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .feature-description {
        color: #ABABBB !important;
    }
    
    .hero-section {
        background: linear-gradient(90deg, #1E1F2C 0%, #2D2E3A 100%);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-align: center;
        border: 1px solid #3A3B45;
    }
    
    .logo-animated {
        font-size: 5rem;
        font-weight: bold;
        color: #4EFB79;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px rgba(78, 251, 121, 0.5);
        animation: glow 1.5s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 5px #4EFB79, 0 0 10px #4EFB79;
        }
        to {
            text-shadow: 0 0 10px #4EFB79, 0 0 20px #4EFB79, 0 0 30px #4EFB79;
        }
    }
    
    .stat-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4EFB79;
    }
    
    .stat-label {
        color: #E1E1E6;
    }
    
    .testimonial {
        font-style: italic;
        color: #E1E1E6;
        text-align: center;
        margin: 2rem 0;
        padding: 1rem;
        background-color: rgba(78, 251, 121, 0.05);
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="home-container">', unsafe_allow_html=True)
    
    # Hero section with animated logo
    st.markdown("""
    <div class="hero-section">
        <div class="logo-animated">codeX</div>
        <h2 class="home-subtitle">Your AI-Powered Coding Companion</h2>
        <p style="color: #ABABBB; margin-bottom: 1.5rem;">Transform your coding experience with advanced AI assistance, real-time insights, and powerful code optimization.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown(f'<h1 class="home-title">Welcome, {st.session_state.username}!</h1>', unsafe_allow_html=True)
    
    # Stats section
    st.markdown("""
    <div class="stat-container">
        <div class="stat-item">
            <div class="stat-number">100+</div>
            <div class="stat-label">Programming Languages</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">24/7</div>
            <div class="stat-label">AI Assistance</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">5M+</div>
            <div class="stat-label">Developers Trust Us</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Choose a feature to get started:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✨</div>
            <h3 class="feature-title">Code Editor</h3>
            <p class="feature-description">Write, analyze, and optimize your code with AI-powered suggestions and improvements.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Open Code Editor", key="open_editor"):
            st.session_state.current_page = "code_editor"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3 class="feature-title">AI Chatbot</h3>
            <p class="feature-description">Get instant help, answers, and guidance about programming from our AI assistant.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Open Chatbot", key="open_chatbot"):
            st.session_state.current_page = "chatbot"
            st.rerun()
    
    # Testimonial
    st.markdown("""
    <div class="testimonial">
        "codeX has transformed how I approach coding problems. The AI assistance is like having a senior developer by your side 24/7."
        <br>- Professional Developer
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ for developers") 