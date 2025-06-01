import json
from utils.parser_utils import detect_format, detect_intent
from memory.memory_store import MemoryStore
from agents.email_agent import process_email
from agents.json_agent import process_json
from agents.pdf_agent import process_pdf

memory = MemoryStore()

def classify_and_route(input_data: str, source: str = "unknown"):
    format_type = detect_format(input_data)
    intent = detect_intent(input_data)

    memory.log_entry({
        "source": source,
        "format": format_type,
        "intent": intent
    })

    if format_type == "Email":
        return process_email(input_data, memory)
    elif format_type == "PDF":
        return process_pdf(input_data, memory)
    elif format_type == "JSON":
        json_data = json.loads(input_data)
        return process_json(json_data, memory)
    else:
        return {"error": "Unsupported format or agent not implemented"}
