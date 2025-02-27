import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import os
import json
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.data_loader import load_titanic_dataset
from app.utils.visualizations import (
    plot_age_histogram, 
    plot_fare_histogram, 
    plot_gender_distribution,
    plot_embarkation_count,
    plot_survival_by_class,
    plot_survival_count,
    plot_age_vs_fare,
    plot_correlation_heatmap
)
# Set page config
st.set_page_config(
    page_title="Titanic Dataset Chatbot",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define API endpoint (local FastAPI server)
API_ENDPOINT = "http://localhost:8000"

# App title and description
st.title("🚢 Titanic Dataset Chatbot")
st.markdown("""
Ask questions about the Titanic dataset in plain English and get both text answers and visualizations.
This app uses FastAPI on the backend with a LangChain-powered agent to process your questions.
""")

# Load API key from environment or let user input one
api_key = os.environ.get("OPENAI_API_KEY", "")
with st.sidebar:
    st.header("Settings")
    user_api_key = st.text_input("OpenAI API Key (optional)", value=api_key, type="password")
    
    st.header("About the Dataset")
    try:
        info_response = requests.get(f"{API_ENDPOINT}/dataset-info")
        if info_response.status_code == 200:
            dataset_info = info_response.json()
            st.write(f"Total passengers: {dataset_info['total_passengers']}")
            st.write(f"Survived: {dataset_info['survived_count']} ({dataset_info['survival_rate']})")
            
            st.subheader("Sample Features")
            features = ", ".join(dataset_info["features"])
            st.write(f"The dataset includes: {features}")
            
            # Show missing values
            st.subheader("Missing Values")
            missing = {k: v for k, v in dataset_info["missing_values"].items() if v > 0}
            if missing:
                for col, count in missing.items():
                    st.write(f"- {col}: {count} missing values")
            else:
                st.write("No missing values")
    except Exception as e:
        st.error(f"Could not connect to API: {str(e)}")
        st.info("Make sure the FastAPI server is running on http://localhost:8000")

# Example questions
st.sidebar.header("Example Questions")
example_questions = [
    "What percentage of passengers were male on the Titanic?",
    "Show me a histogram of passenger ages",
    "What was the average ticket fare?",
    "How many passengers embarked from each port?",
    "What was the survival rate by passenger class?",
    "Did women have a higher survival rate than men?"
]
for q in example_questions:
    if st.sidebar.button(q):
        st.session_state.query = q

# Initialize query session state if not exists
if "query" not in st.session_state:
    st.session_state.query = ""

# User input
query = st.text_input("Ask a question about the Titanic:", value=st.session_state.query)

# Process the query
if query:
    # Show a spinner while processing
    with st.spinner("Processing your question..."):
        try:
            # Prepare the request data
            payload = {
                "query": query,
                "api_key": user_api_key if user_api_key else None
            }
            
            # Send request to our FastAPI backend
            response = requests.post(f"{API_ENDPOINT}/query", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                # Display the answer
                st.markdown("### Answer")
                st.write(result["answer"])
                
                # Display visualization if available
                if result["visualization_type"]:
                    st.markdown("### Visualization")
                    
                    # Based on the visualization type, call the appropriate function
                    if result["visualization_type"] == "age_histogram":
                        fig = plot_age_histogram()
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif result["visualization_type"] == "fare_histogram":
                        fig = plot_fare_histogram()
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif result["visualization_type"] == "gender_distribution":
                        fig = plot_gender_distribution()
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif result["visualization_type"] == "embarkation_count":
                        fig = plot_embarkation_count()
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif result["visualization_type"] == "survival_by_class":
                        fig = plot_survival_by_class()
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif result["visualization_type"] == "survival_count":
                        fig = plot_survival_count()
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif result["visualization_type"] == "age_vs_fare":
                        fig = plot_age_vs_fare()
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif result["visualization_type"] == "correlation_heatmap":
                        fig = plot_correlation_heatmap()
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"Error from API: {response.text}")
        
        except Exception as e:
            st.error(f"Error connecting to the backend: {str(e)}")
            st.info("Make sure the FastAPI server is running on http://localhost:8000")

# Display the dataset (initially collapsed)
with st.expander("View Raw Dataset"):
    df = load_titanic_dataset()
    st.dataframe(df)

# Footer
st.markdown("---")
st.markdown("Powered by FastAPI, LangChain, and Streamlit")