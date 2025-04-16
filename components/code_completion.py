import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

openai.api_key = api_key

def get_code_suggestions(code):
    """Get complete code suggestions using OpenAI"""
    try:
        # Get completion from OpenAI using gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a Python code completion assistant. 
                Analyze the incomplete code and provide a complete, working version of the code.
                Follow these rules:
                1. Return ONLY the Python code, with no explanations or markdown formatting
                2. If you need to explain anything, add it as Python comments at the end of the code
                3. Ensure the code is properly formatted and indented
                4. Include all necessary imports
                5. Add proper error handling
                6. Make sure the code is executable as is"""},
                {"role": "user", "content": f"""Complete this Python code:
{code}"""}
            ],
            max_tokens=1000,
            temperature=0.2
        )
        
        # Extract the complete code suggestion
        complete_code = response.choices[0].message.content.strip()
        
        # Clean up the code
        # Remove any markdown formatting if present
        if complete_code.startswith("```python"):
            complete_code = complete_code[9:]
        if complete_code.endswith("```"):
            complete_code = complete_code[:-3]
        
        # Ensure the code ends with a newline
        if not complete_code.endswith('\n'):
            complete_code += '\n'
        
        return complete_code.strip()
    except Exception as e:
        st.error(f"Error getting suggestions: {str(e)}")
        return code

def code_completion_suggestions(code):
    """Display complete code suggestions"""
    if not code:
        return code
    
    # Get complete code suggestion
    complete_code = get_code_suggestions(code)
    
    return complete_code 