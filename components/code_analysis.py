import streamlit as st
import openai
import os
from dotenv import load_dotenv
import math  # Add common imports
import random
import datetime
import json
import re

# Load environment variables
load_dotenv()

# Set OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

openai.api_key = api_key

def analyze_code(code):
    """Analyze code quality and provide confidence rating"""
    try:
        # Get analysis from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a Python code analysis assistant. 
                Analyze the provided code and provide:
                1. A confidence score (0-100)
                2. Key strengths
                3. Potential issues
                4. Improvement suggestions
                
                Format your response as a JSON object with these keys:
                - confidence_score: number between 0-100
                - strengths: array of strings
                - issues: array of strings
                - improvements: array of strings
                
                Consider these aspects in your analysis:
                - Code structure and organization
                - Error handling
                - Performance considerations
                - Python best practices
                - Code readability
                - Proper use of imports
                
                Be specific and provide actionable feedback."""},
                {"role": "user", "content": f"""Analyze this Python code:
{code}"""}
            ],
            max_tokens=1000,
            temperature=0.2
        )
        
        # Extract the analysis
        analysis = response.choices[0].message.content.strip()
        
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', analysis, re.DOTALL)
        if json_match:
            analysis = json_match.group(0)
        
        try:
            analysis_data = json.loads(analysis)
            return analysis_data
        except json.JSONDecodeError:
            # If the response isn't valid JSON, create a default structure
            return {
                "confidence_score": 50,
                "strengths": ["Code is syntactically correct"],
                "issues": ["Unable to parse detailed analysis"],
                "improvements": ["Check the code structure and formatting"]
            }
            
    except Exception as e:
        st.error(f"Error analyzing code: {str(e)}")
        return {
            "confidence_score": 0,
            "strengths": [],
            "issues": [f"Error during analysis: {str(e)}"],
            "improvements": ["Try again later or check your code"]
        }

def display_analysis(analysis_data):
    """Display the code analysis results"""
    # Confidence Score with color
    score = analysis_data.get("confidence_score", 0)
    if score >= 80:
        color = "green"
    elif score >= 60:
        color = "orange"
    else:
        color = "red"
    
    st.markdown(f"### Code Confidence Score: <span style='color:{color}'>{score}/100</span>", unsafe_allow_html=True)
    
    # Strengths
    st.markdown("#### 🟢 Strengths")
    for strength in analysis_data.get("strengths", []):
        st.markdown(f"- {strength}")
    
    # Issues
    st.markdown("#### 🔴 Potential Issues")
    for issue in analysis_data.get("issues", []):
        st.markdown(f"- {issue}")
    
    # Improvements
    st.markdown("#### 💡 Suggested Improvements")
    for improvement in analysis_data.get("improvements", []):
        st.markdown(f"- {improvement}") 