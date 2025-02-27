import os
import sys
import subprocess

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def start_servers():
    """Start both servers in separate terminals"""
    print("Starting servers in separate terminals...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # For Windows
    if os.name == 'nt':
        subprocess.Popen(['start', 'cmd', '/k', 'python', '-m', 'uvicorn', 'app.api:app', '--host', '0.0.0.0', '--port', '8000'], shell=True)
        subprocess.Popen(['start', 'cmd', '/k', 'streamlit', 'run', 'app/streamlit_app.py'], shell=True)
    
    # For Unix/Linux/MacOS
    else:
        subprocess.Popen(['gnome-terminal', '--', 'python', '-m', 'uvicorn', 'app.api:app', '--host', '0.0.0.0', '--port', '8000'])
        subprocess.Popen(['gnome-terminal', '--', 'streamlit', 'run', 'app/streamlit_app.py'])

if __name__ == "__main__":
    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable not set.")
        print("You can still run the app, but you'll need to input an API key in the Streamlit interface.")
        print("Alternatively, set it using: set OPENAI_API_KEY=your_api_key_here")
    
    start_servers()
