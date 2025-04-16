import streamlit as st
from streamlit_ace import st_ace
from config.database import save_user_code_snippet, get_user_code_snippets, delete_user_code_snippet
from code_runner import run_code
from components.navbar import navbar
from components.code_completion import code_completion_suggestions
from components.code_analysis import analyze_code, display_analysis
from components.resource_recommendations import get_resource_recommendations, display_recommendations
import os
from datetime import datetime
import pandas as pd
import time

def execute_code(code):
    """Execute the code and return its output"""
    import sys
    from io import StringIO
    import contextlib
    
    # Create StringIO object to capture output
    output = StringIO()
    
    # Redirect stdout to our StringIO object
    with contextlib.redirect_stdout(output):
        try:
            # Create a local environment for execution
            local_env = {}
            exec(code, {}, local_env)
            return output
        except Exception as e:
            return f"Error: {str(e)}"

def code_editor_page():
    # Add the main navbar
    navbar()
    
    # Check if user is logged in
    if 'username' not in st.session_state:
        st.error("Please log in to use the code editor")
        st.stop()
    
    # Custom CSS for better UI - matching the provided UI image
    st.markdown("""
    <style>
    /* Main color variables */
    :root {
        --bg-dark: #2D2E3A;
        --bg-darker: #1E1F2C;
        --accent-green: #4EFB79;
        --text-light: #E1E1E6;
        --sidebar-bg: #2D2E3A;
        --editor-bg: #1E1F2C;
        --tab-bg: #2D2E3A;
    }
    
    /* Main container */
    .main {
        background-color: var(--bg-darker);
        color: var(--text-light);
    }
    
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0;
        background-color: var(--bg-darker);
    }
    
    /* Streamlit native elements override */
    .stApp {
        background-color: var(--bg-darker);
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Header / Navigation */
    .stDeployButton {
        display: none !important;
    }
    
    header {
        background-color: var(--bg-dark) !important;
        border-bottom: 1px solid #3A3B45;
    }
    
    /* Feature Navigation Bar */
    .nav-container {
        background-color: var(--bg-dark);
        padding: 10px 20px;
        border-radius: 0;
        margin-bottom: 0;
        border-bottom: 1px solid #3A3B45;
        display: flex;
        justify-content: space-between;
    }
    
    /* Feature Buttons */
    .feature-button {
        background-color: var(--bg-dark);
        color: var(--accent-green);
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 14px;
    }
    
    .feature-button:hover {
        background-color: #3A3B45;
    }
    
    /* Code Editor Container */
    .editor-container {
        background-color: var(--editor-bg);
        padding: 0;
        border-radius: 0;
        border-top: 2px solid var(--accent-green);
    }
    
    /* Output Container */
    .output-container {
        background-color: var(--editor-bg);
        padding: 15px;
        border-radius: 0;
        border-top: 1px solid #3A3B45;
    }
    
    /* Filename tabs */
    .tab-container {
        display: flex;
        background-color: var(--tab-bg);
        padding: 0;
        border-bottom: 1px solid #3A3B45;
    }
    
    .tab {
        padding: 8px 20px;
        background-color: var(--editor-bg);
        color: var(--text-light);
        border-right: 1px solid #3A3B45;
        font-size: 13px;
    }
    
    .tab-active {
        border-top: 2px solid var(--accent-green);
        background-color: var(--editor-bg);
    }
    
    /* Saved Code Items */
    .saved-code-item {
        background-color: var(--editor-bg);
        padding: 12px;
        margin-bottom: 10px;
        border-radius: 4px;
        border-left: 2px solid var(--accent-green);
    }
    
    /* Delete Button */
    .delete-button {
        background-color: #3A3B45;
        color: var(--text-light);
        border: none;
        padding: 5px 10px;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 12px;
        margin-top: 8px;
    }
    
    .delete-button:hover {
        background-color: #FF5A5A;
    }
    
    /* Success Messages */
    .stSuccess {
        background-color: #164B2B !important;
        color: var(--accent-green) !important;
        border: 1px solid var(--accent-green) !important;
        padding: 8px !important;
    }
    
    /* Error Messages */
    .stError {
        background-color: #4E2329 !important;
        color: #FF5A5A !important;
        border: 1px solid #FF5A5A !important;
        padding: 8px !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: var(--bg-dark) !important;
        color: var(--text-light) !important;
        border-radius: 4px !important;
    }
    
    /* Code Block Styling */
    pre {
        background-color: var(--editor-bg) !important;
        border-radius: 4px !important;
        padding: 10px !important;
        font-family: 'Consolas', 'Monaco', monospace !important;
    }
    
    /* Title Styling */
    h1, h2 {
        color: var(--accent-green) !important;
        font-weight: 500 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        color: var(--text-light) !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    /* Button override */
    button {
        border-radius: 4px !important;
    }
    
    .stButton > button {
        background-color: var(--bg-dark) !important;
        color: var(--accent-green) !important;
        border: 1px solid #3A3B45 !important;
    }
    
    .stButton > button:hover {
        border-color: var(--accent-green) !important;
        background-color: #3A3B45 !important;
    }
    
    .output-area {
        background-color: #2D2E3A;
        padding: 1rem;
        border-radius: 6px;
        font-family: monospace;
        color: #4EFB79;
        border-left: 2px solid #4EFB79;
        margin: 1rem 0;
        white-space: pre-wrap;
    }
    
    .error-output {
        color: #FF6B6B;
        border-left-color: #FF6B6B;
    }
    
    .success-message {
        color: #4EFB79;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown('<h2 style="color: #4EFB79; margin-bottom: 1rem;">Code Editor</h2>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'code' not in st.session_state:
        st.session_state.code = ""
    if 'show_suggestions' not in st.session_state:
        st.session_state.show_suggestions = False
    if 'suggested_code' not in st.session_state:
        st.session_state.suggested_code = ""
    if 'editor_key' not in st.session_state:
        st.session_state.editor_key = 0
    if 'show_analysis' not in st.session_state:
        st.session_state.show_analysis = False
    if 'analysis_data' not in st.session_state:
        st.session_state.analysis_data = None
    if 'show_resources' not in st.session_state:
        st.session_state.show_resources = False
    if 'resource_data' not in st.session_state:
        st.session_state.resource_data = None
    if 'active_file' not in st.session_state:
        st.session_state.active_file = "main.py"
    
    # Feature Navigation Bar styled like the image
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("💾 Save", key="nav_save"):
            if st.session_state.code and 'username' in st.session_state:
                save_user_code_snippet(st.session_state.username, st.session_state.code)
                st.success("Code saved successfully!")
    
    with col2:
        if st.button("▶️ Run", key="nav_run"):
            if st.session_state.code:
                st.session_state.output = run_code(st.session_state.code)
                st.rerun()
    
    with col3:
        if st.button("✨ Complete", key="nav_suggest"):
            st.session_state.show_suggestions = True
            st.session_state.suggested_code = code_completion_suggestions(st.session_state.code)
            st.rerun()
    
    with col4:
        if st.button("📊 Analyze", key="nav_analyze"):
            st.session_state.show_analysis = True
            st.session_state.analysis_data = analyze_code(st.session_state.code)
            st.rerun()
    
    with col5:
        if st.button("📚 Resources", key="nav_resources"):
            st.session_state.show_resources = True
            st.session_state.resource_data = get_resource_recommendations(st.session_state.code)
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # File Tabs similar to the image
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="tab tab-active">{st.session_state.active_file}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Layout
    col_editor, col_output = st.columns([2, 1])
    
    with col_editor:
        st.markdown('<div class="editor-container">', unsafe_allow_html=True)
        # No header needed here to match the image
        code = st_ace(
            language="python",
            theme="monokai",
            key=f"code_editor_{st.session_state.editor_key}",
            height=400,
            font_size=14,
            show_gutter=True,
            show_print_margin=True,
            wrap=True,
            auto_update=True,
            value=st.session_state.code
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Update session state with new code
        if code != st.session_state.code:
            st.session_state.code = code
    
    # Show suggestions in a popup if requested
    if st.session_state.show_suggestions:
        with st.expander("Complete Code Suggestion", expanded=True):
            st.code(st.session_state.suggested_code, language="python")
            col_apply, col_close = st.columns(2)
            with col_apply:
                if st.button("Apply Suggestion"):
                    st.session_state.code = st.session_state.suggested_code
                    st.session_state.editor_key += 1
                    st.session_state.show_suggestions = False
                    st.rerun()
            with col_close:
                if st.button("Close"):
                    st.session_state.show_suggestions = False
                    st.rerun()
    
    # Show analysis in a popup if requested
    if st.session_state.show_analysis:
        with st.expander("Code Analysis", expanded=True):
            if st.session_state.analysis_data:
                display_analysis(st.session_state.analysis_data)
            if st.button("Close Analysis"):
                st.session_state.show_analysis = False
                st.rerun()
    
    # Show resources in a popup if requested
    if st.session_state.show_resources:
        with st.expander("Learning Resources", expanded=True):
            if st.session_state.resource_data:
                display_recommendations(st.session_state.resource_data)
            if st.button("Close Resources"):
                st.session_state.show_resources = False
                st.rerun()
    
    with col_output:
        st.markdown('<div class="output-container">', unsafe_allow_html=True)
        st.markdown("### Output")
        if 'output' in st.session_state:
            if st.session_state.output.startswith("Error:"):
                st.markdown(f'<div class="output-area error-output">{st.session_state.output}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-message">Code executed successfully!</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="output-area">{st.session_state.output}</div>', unsafe_allow_html=True)
        
        # Saved Code Section
        if 'username' in st.session_state:
            st.markdown("### Saved Code")
            snippets = get_user_code_snippets(st.session_state.username)
            if not snippets.empty:
                snippets['created_at'] = pd.to_datetime(snippets['created_at'])
                snippets['date'] = snippets['created_at'].dt.date
                for date, group in snippets.groupby('date'):
                    with st.expander(f"Code from {date.strftime('%B %d, %Y')}"):
                        for _, snippet in group.iterrows():
                            st.markdown('<div class="saved-code-item">', unsafe_allow_html=True)
                            st.code(snippet['code'], language="python")
                            if st.button("🗑️", key=f"delete_{snippet['id']}"):
                                delete_user_code_snippet(snippet['id'])
                                st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) 