# 🧠 Multi-Agent AI Classification & Routing System

This project is a simple multi-agent system that accepts documents (PDF, JSON, or Email), figures out what type they are and what they’re about, and then sends them to the right agent to process. It keeps track of everything using a shared memory.

---

## ✅ What It Does

- **Classifier Agent**: Checks file type (PDF/JSON/Email) and its intent (Invoice, Complaint, etc.)
- **JSON Agent**: Reads and cleans up JSON data, checks for missing or wrong fields
- **Email Agent**: Reads emails, pulls out useful info like sender and urgency
- **Memory Module**: Saves key info like source, type, and results (uses Redis or SQLite)
- **LLM Support**: Uses the `gemma3:1b` model from Ollama to help with classification

---

## 🧰 Tech Used

- Python 3.10+
- SQLite (shared memory)
- Ollama (runs `gemma3:1b` locally)
- PDFPlumber, email parser tools, etc.

---

## Setup

1. **Install Virtual Env & Setup Virtualenv:**
    ```bash
    virtualenv venv
    ```
    

2. **Activate venv & Install Packages to venv:**
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ How to Run

1. **Start Redis (if you're using Redis):**
   ```bash
   redis-server
   ```

2. **Start Ollama with gemma3:1b:**
    ```bash
    ollama run gemma3:1b
    ```

3. **Start the app (Streamlit):**
    ```bash
    streamlit run main.py
    ```


## 📌 Example Flow

1. You upload a file (PDF, JSON, or Email).

2. Classifier decides what it is and what it wants.

3. Routes it to the right agent.

4. Agent pulls info.

5. Memory saves the data.