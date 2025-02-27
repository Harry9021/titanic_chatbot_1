import os
import sys
import subprocess
import time
import webbrowser
import threading

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def start_fastapi():
    """Start the FastAPI server"""
    print("Starting FastAPI server...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.Popen(["python", "-m", "uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"])

def start_streamlit():
    """Start the Streamlit frontend"""
    print("Starting Streamlit frontend...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.Popen(["streamlit", "run", "app/streamlit_app.py"])

def open_browser():
    """Open the browser to the Streamlit app"""
    print("Opening browser...")
    time.sleep(5)  # Give time for servers to start
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable not set.")
        print("You can still run the app, but you'll need to input an API key in the Streamlit interface.")
        print("Alternatively, set it using: set OPENAI_API_KEY=your_api_key_here")
    
    # Start FastAPI server in a separate thread
    fastapi_thread = threading.Thread(target=start_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()
    
    # Start Streamlit frontend
    streamlit_thread = threading.Thread(target=start_streamlit)
    streamlit_thread.daemon = True
    streamlit_thread.start()
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")