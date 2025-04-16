import streamlit as st

st.title("Pattern Generator")

# Add a slider for pattern size
n = st.slider("Select pattern size", min_value=1, max_value=10, value=5)

# Custom CSS for pattern display
st.markdown("""
<style>
.pattern {
    background-color: #2D2E3A;
    padding: 20px;
    border-radius: 5px;
    font-family: monospace;
    color: #4EFB79;
    border-left: 2px solid #4EFB79;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Generate and display pattern
pattern = ""
for i in range(1, n + 1):
    pattern += '*' * i + '\n'

st.markdown(f'<pre class="pattern">{pattern}</pre>', unsafe_allow_html=True) 