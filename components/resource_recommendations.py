import streamlit as st
import openai
import os
from dotenv import load_dotenv
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

def get_resource_recommendations(code):
    """Get relevant resource recommendations for the code"""
    try:
        # Get recommendations from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a Python learning resource assistant. 
                Analyze the provided code and recommend relevant learning resources.
                
                Format your response as a JSON object with these keys:
                - documentation: array of objects with 'title' and 'url' for official Python docs
                - tutorials: array of objects with 'title' and 'url' for learning resources
                - examples: array of objects with 'title' and 'url' for code examples
                - stack_overflow: array of objects with 'title' and 'url' for relevant discussions
                
                Focus on:
                1. Official Python documentation
                2. High-quality tutorials and courses
                3. Practical code examples
                4. Relevant Stack Overflow discussions
                
                Ensure all URLs are valid and accessible."""},
                {"role": "user", "content": f"""Analyze this Python code and recommend learning resources:
{code}"""}
            ],
            max_tokens=1000,
            temperature=0.2
        )
        
        # Extract the recommendations
        recommendations = response.choices[0].message.content.strip()
        
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', recommendations, re.DOTALL)
        if json_match:
            recommendations = json_match.group(0)
        
        try:
            recommendations_data = json.loads(recommendations)
            return recommendations_data
        except json.JSONDecodeError:
            # If the response isn't valid JSON, create a default structure
            return {
                "documentation": [{"title": "Python Official Documentation", "url": "https://docs.python.org/3/"}],
                "tutorials": [{"title": "Python Tutorial", "url": "https://docs.python.org/3/tutorial/"}],
                "examples": [{"title": "Python Code Examples", "url": "https://docs.python.org/3/tutorial/stdlib.html"}],
                "stack_overflow": [{"title": "Python Questions", "url": "https://stackoverflow.com/questions/tagged/python"}]
            }
            
    except Exception as e:
        st.error(f"Error getting recommendations: {str(e)}")
        return {
            "documentation": [],
            "tutorials": [],
            "examples": [],
            "stack_overflow": []
        }

def display_recommendations(recommendations_data):
    """Display the resource recommendations"""
    # Documentation
    if recommendations_data.get("documentation"):
        st.markdown("### 📚 Official Documentation")
        for doc in recommendations_data["documentation"]:
            st.markdown(f"- [{doc['title']}]({doc['url']})")
    
    # Tutorials
    if recommendations_data.get("tutorials"):
        st.markdown("### 📖 Tutorials & Courses")
        for tutorial in recommendations_data["tutorials"]:
            st.markdown(f"- [{tutorial['title']}]({tutorial['url']})")
    
    # Examples
    if recommendations_data.get("examples"):
        st.markdown("### 💻 Code Examples")
        for example in recommendations_data["examples"]:
            st.markdown(f"- [{example['title']}]({example['url']})")
    
    # Stack Overflow
    if recommendations_data.get("stack_overflow"):
        st.markdown("### 🔍 Stack Overflow Discussions")
        for discussion in recommendations_data["stack_overflow"]:
            st.markdown(f"- [{discussion['title']}]({discussion['url']})") 