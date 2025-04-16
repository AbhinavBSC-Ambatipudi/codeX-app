import streamlit as st

def load_app_styles():
    """
    Load global application styles that match the code editor dark theme with neon green accents.
    This function applies the styling to the entire Streamlit application.
    """
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
        --border-color: #3A3B45;
    }
    
    /* Global elements */
    .stApp {
        background-color: var(--bg-darker) !important;
        color: var(--text-light) !important;
    }
    
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Header / Navigation */
    header {
        background-color: var(--bg-dark) !important;
        border-bottom: 1px solid var(--border-color);
    }
    
    /* Hide Streamlit branding */
    .stDeployButton {
        display: none !important;
    }
    
    /* Footer hide */
    footer {
        display: none !important;
    }
    
    /* Text elements */
    h1, h2 {
        color: var(--accent-green) !important;
        font-weight: 500 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3, h4, h5, h6 {
        color: var(--text-light) !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    p, li, ul, ol {
        color: var(--text-light) !important;
    }
    
    /* Streamlit Elements */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: var(--bg-dark) !important;
        color: var(--text-light) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 4px !important;
    }
    
    .stTextInput > div > div > input:focus, 
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-green) !important;
    }
    
    .stCheckbox > div > label > div {
        background-color: var(--bg-dark) !important;
    }
    
    .stCheckbox > div > label > div[data-check="true"] {
        background-color: var(--accent-green) !important;
    }
    
    /* Buttons */
    button {
        border-radius: 4px !important;
    }
    
    .stButton > button {
        background-color: var(--bg-dark) !important;
        color: var(--accent-green) !important;
        border: 1px solid var(--border-color) !important;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        border-color: var(--accent-green) !important;
        background-color: #3A3B45 !important;
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Cards and Containers */
    .stAlert {
        background-color: var(--bg-dark) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-light) !important;
    }
    
    /* Success Messages */
    .stSuccess {
        background-color: #164B2B !important;
        color: var(--accent-green) !important;
        border: 1px solid var(--accent-green) !important;
        padding: 8px !important;
        border-radius: 4px !important;
    }
    
    /* Error Messages */
    .stError {
        background-color: #4E2329 !important;
        color: #FF5A5A !important;
        border: 1px solid #FF5A5A !important;
        padding: 8px !important;
        border-radius: 4px !important;
    }
    
    /* Info Messages */
    .stInfo {
        background-color: #1E3A5F !important;
        color: #6BBBFF !important;
        border: 1px solid #6BBBFF !important;
        padding: 8px !important;
        border-radius: 4px !important;
    }
    
    /* Warning Messages */
    .stWarning {
        background-color: #553A10 !important;
        color: #FFC857 !important;
        border: 1px solid #FFC857 !important;
        padding: 8px !important;
        border-radius: 4px !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: var(--bg-dark) !important;
        color: var(--text-light) !important;
        border-radius: 4px !important;
    }
    
    .streamlit-expanderContent {
        background-color: var(--bg-darker) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
    }
    
    /* Data elements */
    .stDataFrame, .stTable {
        background-color: var(--bg-dark) !important;
    }
    
    .stDataFrame td, .stDataFrame th, .stTable td, .stTable th {
        background-color: var(--bg-dark) !important;
        color: var(--text-light) !important;
        border-color: var(--border-color) !important;
    }
    
    /* Code Block Styling */
    pre {
        background-color: var(--editor-bg) !important;
        border-radius: 4px !important;
        padding: 10px !important;
        font-family: 'Consolas', 'Monaco', monospace !important;
    }
    
    code {
        color: var(--accent-green) !important;
    }
    
    /* ScrollBars */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-darker);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--bg-dark);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--border-color);
    }
    
    /* Sidebar */
    .css-1d391kg, .css-12oz5g7 {
        background-color: var(--sidebar-bg) !important;
    }
    </style>
    """, unsafe_allow_html=True) 