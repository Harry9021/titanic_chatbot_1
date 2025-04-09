# 🚢 Titanic Chatbot – Query & Visualize Titanic Data

A modern **chatbot** for the Titanic dataset that lets you ask natural‑language questions and returns both **text answers** and **interactive visualizations**. Powered by **FastAPI** + **LangChain** on the backend and a sleek **Streamlit** UI.

---

## 🛠 Tech Stack

- **Language**: Python 100%
- **Backend API**: FastAPI, Uvicorn, Pydantic 
- **UI**: Streamlit 
- **LLM & Agents**: LangChain, OpenAI (ChatOpenAI)
- **Data Processing**: pandas, numpy, scikit‑learn
- **Visualizations**: Plotly, matplotlib, seaborn
---

## 🎯 Features

- 🤖 **Natural‑language querying** via a LangChain‑powered FastAPI agent  
- 📊 **Dynamic visualizations**: age/fare histograms, survival heatmaps, correlation plots  
- 🔄 **Dataset loader**: auto‑downloads Titanic CSV if not present citeturn10view0  
- 🔐 **Optional OpenAI API key** for richer LLM responses  
- 🌐 **Interactive Streamlit interface** with sidebar settings and example prompts  

---

## 📂 Project Structure

```
titanic_chatbot_1/
├── .devcontainer/           # Dev container config
├── app/                     # Application package
│   ├── api.py               # FastAPI endpoints
│   ├── streamlit_app.py     # Streamlit UI
│   ├── data/                # Titanic CSV dataset
│   └── utils/               # Helpers: agent, data_loader, visualizations
├── main.py                  # Orchestrator: starts both servers
├── requirements.txt         # Python deps citeturn7view0
└── packages.txt             # System deps (python3‑dev) citeturn6view0
```

---

## ⚙️ Prerequisites

- **Python** ≥ 3.8  
- **(Linux)** `python3-dev`
- **OpenAI API Key** (optional): set `OPENAI_API_KEY` env var for LLM support  

---

## 🚀 Quick Start

1. **Clone the repo**  
   ```bash
   git clone https://github.com/Harry9021/titanic_chatbot_1.git
   cd titanic_chatbot_1
   ```
2. **Install Python dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app**  
   ```bash
   python main.py
   ```
   - **API**: http://localhost:8000  
   - **UI**:  http://localhost:8501  

---

## 🤝 Contributing

1. Fork & clone  
2. Create a branch:  
   ```bash
   git checkout -b feature/my‑awesome‑feature
   ```
3. Commit your changes:  
   ```bash
   git commit -m "feat: add awesome feature"
   ```
4. Push & open a PR 🚀  

---

Made with ❤️ by [@Harry9021](https://github.com/Harry9021)
