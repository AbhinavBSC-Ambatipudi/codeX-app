import streamlit as st
from components.navbar import navbar

def pattern_page():
    # Add the navbar
    navbar()
    
    st.title("Pattern Generator")
    
    # Pattern size input
    n = st.slider("Select pattern size", 1, 10, 5)
    
    # Generate pattern
    pattern = ""
    for i in range(1, n + 1):
        pattern += "* " * i + "\n"
    
    # Display pattern
    st.markdown("### Output:")
    st.code(pattern, language=None)

if __name__ == "__main__":
    pattern_page() 