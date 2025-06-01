from agents.classifier_agent import classify_and_route
from memory.memory_store import MemoryStore

def read_file(path):
    if path.lower().endswith(".pdf"):
        with open(path, "rb") as f:
            return f.read()  # return bytes for PDF
    else:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

if __name__ == "__main__":
    input_path = "samples/sample_document.pdf"  # Change to other file to test
    content = read_file(input_path)
    
    print("Input loaded:", input_path)
    result = classify_and_route(content, source=input_path)
    
    print("\n🔍 Final Output:")
    print(result)

    # Print memory log
    mem = MemoryStore()
    print("\n🧠 Memory Logs:")
    for log in mem.get_logs():
        print(log)
