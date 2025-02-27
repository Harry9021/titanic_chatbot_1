import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import io
import base64
import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.utils.data_loader import load_titanic_dataset

def get_base64_encoded_figure(fig):
    """Convert matplotlib figure to base64 encoded string for displaying in Streamlit"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return img_str

def plot_survival_count():
    """Plot count of survived vs perished passengers"""
    df = load_titanic_dataset()
    fig = plt.figure(figsize=(10, 6))
    sns.countplot(x='Survived', data=df, palette='viridis')
    plt.title('Survival Count (0 = No, 1 = Yes)')
    plt.xlabel('Survived')
    plt.ylabel('Count')
    return fig

def plot_gender_distribution():
    """Plot gender distribution of passengers"""
    df = load_titanic_dataset()
    fig = px.pie(df, names='Sex', title='Gender Distribution')
    return fig

def plot_age_histogram():
    """Plot histogram of passenger ages"""
    df = load_titanic_dataset()
    fig = px.histogram(df, x='Age', nbins=20, title='Distribution of Passenger Ages')
    fig.update_layout(xaxis_title='Age', yaxis_title='Count')
    return fig

def plot_fare_histogram():
    """Plot histogram of ticket fares"""
    df = load_titanic_dataset()
    fig = px.histogram(df, x='Fare', nbins=30, title='Distribution of Ticket Fares')
    fig.update_layout(xaxis_title='Fare', yaxis_title='Count')
    return fig

def plot_embarkation_count():
    """Plot count of passengers by embarkation port"""
    df = load_titanic_dataset()
    # Replace port codes with more readable names
    port_names = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}
    df['Embarkation Port'] = df['Embarked'].map(port_names)
    
    fig = px.bar(
        df.groupby('Embarkation Port').size().reset_index(name='Count'), 
        x='Embarkation Port', 
        y='Count',
        title='Passengers by Embarkation Port'
    )
    return fig

def plot_survival_by_class():
    """Plot survival rate by passenger class"""
    df = load_titanic_dataset()
    survival_by_class = df.groupby('Pclass')['Survived'].mean().reset_index()
    survival_by_class['Survival Rate'] = survival_by_class['Survived'] * 100
    
    fig = px.bar(
        survival_by_class, 
        x='Pclass', 
        y='Survival Rate',
        title='Survival Rate by Passenger Class',
        labels={'Pclass': 'Passenger Class', 'Survival Rate': 'Survival Rate (%)'}
    )
    return fig

def plot_age_vs_fare():
    """Create a scatter plot of age vs fare with survival indicated by color"""
    df = load_titanic_dataset()
    fig = px.scatter(
        df.dropna(subset=['Age', 'Fare']), 
        x='Age', 
        y='Fare', 
        color='Survived',
        opacity=0.7,
        color_discrete_map={0: 'red', 1: 'green'},
        title='Age vs Fare (colored by survival)'
    )
    return fig

def plot_correlation_heatmap():
    """Create a correlation heatmap of numeric features"""
    df = load_titanic_dataset()
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    
    fig = px.imshow(
        numeric_df.corr(),
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )
    return fig