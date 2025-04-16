import streamlit as st

# Simple healthcheck endpoint for monitoring
def healthcheck():
    return {"status": "ok", "version": "1.0.0"}

if __name__ == "__main__":
    st.json(healthcheck()) 