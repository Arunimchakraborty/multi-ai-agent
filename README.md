# 🧠 Multi-Agent AI Classification & Routing System

This project is a simple multi-agent system that accepts documents (PDF, JSON, or Email), figures out what type they are and what they’re about, and then sends them to the right agent to process. It keeps track of everything using a shared memory.

---

## ✅ What It Does

- **Classifier Agent**: Checks file type (PDF/JSON/Email) and its intent (Invoice, Complaint, etc.)
- **JSON Agent**: Reads and cleans up JSON data, checks for missing or wrong fields
- **Email Agent**: Reads emails, pulls out useful info like sender and urgency
- **Memory Module**: Saves key info like source, type, and results (uses Redis or SQLite)
- **LLM Support**: Uses the `gemma:1b` model from Ollama to help with classification

---

## 🧰 Tech Used

- Python 3.10+
- FastAPI (for APIs)
- Redis or SQLite (shared memory)
- Ollama (runs `gemma:1b` locally)
- PDFPlumber, email parser tools, etc.

---

## 📁 Folder Structure

```
project-root/
│
├── agents/
│   ├── classifier_agent.py
│   ├── json_agent.py
│   └── email_agent.py
│
├── memory/
│   ├── redis_store.py
│   └── sqlite_store.py
│
├── utils/
│   ├── file_loader.py
│   ├── format_detector.py
│   └── intent_detector.py
│
├── data/
│   ├── sample_inputs/
│   └── output_logs/
│
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```


---

## ▶️ How to Run

1. **Start Redis (if you're using Redis):**
   ```bash
   redis-server
   ```

2. **Start Ollama with gemma:1b:**
    ```bash
    ollama run gemma:1b
    ```

3. **Start the app (FastAPI):**
    ```bash
    uvicorn main:app --reload
    ```


## 📌 Example Flow

1. You upload a file (PDF, JSON, or Email).

2. Classifier decides what it is and what it wants.

3. Routes it to the right agent.

4. Agent pulls info.

5. Memory saves the data.