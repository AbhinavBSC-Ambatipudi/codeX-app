import streamlit as st
import openai
import os
from dotenv import load_dotenv
from components.navbar import navbar

# Load environment variables
load_dotenv()

# Set OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

openai.api_key = api_key

def get_ai_response(messages):
    """Get response from OpenAI API"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error: {str(e)}"

def execute_code(code):
    """Execute code and return the output"""
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
        except Exception as e:
            return f"Error: {str(e)}"
    
    return output.getvalue()

def chatbot_page():
    # Add the main navbar
    navbar()
    
    # Check if user is logged in
    if 'username' not in st.session_state:
        st.error("Please log in to use the chatbot")
        st.stop()
    
    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful AI assistant focused on programming and coding. You help users with programming questions, debugging, and learning to code."},
            {"role": "assistant", "content": "Hi there! I'm your AI programming assistant. How can I help you with your coding questions today?"}
        ]
    
    # Initialize code output if it doesn't exist
    if "code_output" not in st.session_state:
        st.session_state.code_output = None
    
    # Custom CSS for chatbot page
    st.markdown("""
    <style>
    .chat-container {
        background-color: #1E1F2C;
        border-radius: 8px;
        border: 1px solid rgba(78, 251, 121, 0.2);
        box-shadow: 0 0 10px rgba(78, 251, 121, 0.1);
        margin-top: 1rem;
        margin-bottom: 1rem;
        padding: 1rem;
    }
    
    .chat-messages {
        max-height: 400px;
        overflow-y: auto;
    }
    
    .message {
        margin-bottom: 0.8rem;
        padding: 0.8rem;
        border-radius: 6px;
        animation: fadeIn 0.3s ease-in;
    }
    
    .user-message {
        background-color: #2D2E3A;
        border-left: 2px solid #4EFB79;
        margin-left: 1rem;
    }
    
    .ai-message {
        background-color: #2D2E3A;
        border-left: 2px solid #6BBBFF;
        margin-right: 1rem;
    }
    
    .message-header {
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    
    .user-header {
        color: #4EFB79;
    }
    
    .ai-header {
        color: #6BBBFF;
    }
    
    .message-content {
        color: #E1E1E6;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    .stTextArea textarea {
        background-color: #2D2E3A;
        color: #E1E1E6;
        border: 1px solid rgba(78, 251, 121, 0.2);
        border-radius: 6px;
        font-size: 0.9rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #4EFB79;
        box-shadow: 0 0 0 1px #4EFB79;
    }
    
    /* Override all button styles first */
    .stButton > button {
        background-color: #1E1F2C !important;
        color: #4EFB79 !important;
        border: 1px solid #3A3B45 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 4px !important;
    }

    .stButton > button:hover {
        border-color: #4EFB79 !important;
        background-color: #2D2E3A !important;
        color: #4EFB79 !important;
    }

    /* Style for the send button specifically */
    .stButton > button[kind="primary"] {
        background-color: #4EFB79 !important;
        color: #1E1F2C !important;
        border: none !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #3DE668 !important;
        color: #1E1F2C !important;
    }

    /* Clear chat button specific styling */
    .clear-chat .stButton > button {
        background-color: #2D2E3A !important;
        color: #ABABBB !important;
        border: 1px solid #3A3B45 !important;
        font-size: 0.9rem !important;
    }

    .clear-chat .stButton > button:hover {
        background-color: #1E1F2C !important;
        color: #E1E1E6 !important;
        border-color: #4EFB79 !important;
    }
    
    .code-output {
        background-color: #2D2E3A;
        border-radius: 6px;
        padding: 1rem;
        margin-top: 0.5rem;
        font-family: monospace;
        white-space: pre-wrap;
        color: #E1E1E6;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a container for the chat interface
    with st.container():
        st.markdown('<h2 style="color: #4EFB79; margin-bottom: 0.5rem;">AI Programming Assistant</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #ABABBB; margin-bottom: 1rem; font-size: 0.9rem;">Get help with your programming questions and code</p>', unsafe_allow_html=True)
        
        # Display chat messages if they exist
        visible_messages = [m for m in st.session_state.messages if m["role"] != "system"]
        
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        if len(visible_messages) > 0:
            st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
            
            for message in st.session_state.messages:
                if message["role"] != "system":
                    if message["role"] == "user":
                        st.markdown(f"""
                        <div class="message user-message">
                            <div class="message-header user-header">You</div>
                            <div class="message-content">{message["content"]}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # If this message contains code, try to execute it
                        if "```python" in message["content"]:
                            code = message["content"].split("```python")[1].split("```")[0].strip()
                            output = execute_code(code)
                            if output:
                                st.markdown(f"""
                                <div class="message ai-message">
                                    <div class="message-header ai-header">Output</div>
                                    <div class="code-output">{output}</div>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="message ai-message">
                            <div class="message-header ai-header">AI Assistant</div>
                            <div class="message-content">{message["content"]}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-chat">
                <div class="empty-chat-icon">💬</div>
                <p>No messages yet. Start a conversation by typing below!</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Clear chat button with updated styling
        if len(visible_messages) > 0:
            col1, col2 = st.columns([4, 1])
            with col2:
                st.markdown('<div class="clear-chat">', unsafe_allow_html=True)
                if st.button("Clear Chat", help="Clear the current conversation"):
                    st.session_state.messages = [
                        {"role": "system", "content": "You are a helpful AI assistant focused on programming and coding. You help users with programming questions, debugging, and learning to code."}
                    ]
                    st.session_state.code_output = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Tips section
        with st.expander("Tips for better results"):
            st.markdown("""
            - Be specific about your programming language
            - Share relevant code snippets
            - Describe what you've tried
            - Ask for explanations if needed
            """)
        
        # Chat input
        user_input = st.chat_input("Type your message here...")
    
    # Handle user input
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response
        messages_for_api = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        ai_response = get_ai_response(messages_for_api)
        
        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Rerun to update UI
        st.rerun() 