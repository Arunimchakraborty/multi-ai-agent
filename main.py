import streamlit as st
from agents.classifier_agent import classify_and_route
from memory.memory_store import MemoryStore

def read_file(uploaded_file):
    if uploaded_file.name.lower().endswith(".pdf"):
        return uploaded_file.read()  # bytes
    else:
        return uploaded_file.getvalue().decode("utf-8")

def main():
    st.title("Document Classification and Routing")
    
    uploaded_file = st.file_uploader("Upload a PDF or Text document", type=["pdf", "txt", "json", "eml"])
    
    if uploaded_file is not None:
        st.write(f"Loaded file: {uploaded_file.name}")
        
        content = read_file(uploaded_file)
        
        # Classify and route
        result = classify_and_route(content, source=uploaded_file.name)
        
        st.subheader("🔍 Classification Result:")
        st.json(result)
        
        # Display memory logs
        mem = MemoryStore()
        logs = mem.get_logs()
        if logs:
            st.subheader("🧠 Memory Logs:")
            for idx, log in enumerate(logs, start=1):
                st.write(f"Log {idx}: {log}")
        else:
            st.info("No memory logs available.")

if __name__ == "__main__":
    main()
