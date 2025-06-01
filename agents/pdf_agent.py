import json
from utils.parser_utils import extract_text_from_pdf, detect_intent
from utils.llm_utils import query_ollama

def process_pdf(pdf_path: str, memory):
    text = extract_text_from_pdf(pdf_path)

    if not text:
        return {
            "status": "error",
            "message": "Could not extract text from PDF"
        }

    intent = detect_intent(text)

    prompt = (
        "You are an intelligent assistant. Analyze the content of this PDF document and extract any relevant structured fields. "
        "Try to identify the sender, recipient, subject, date, and a brief summary if possible. "
        "Return the result as a JSON object with the keys: sender, recipient, subject, date, summary. "
        "If any fields are missing, return them as null. Only return the JSON object.\n\n"
        f"PDF Content:\n{text}\n\n"
        "Extracted JSON:"
    )

    response = query_ollama(prompt)

    # Clean LLM output
    try:
        structured_data = json.loads(response.strip().removeprefix("```json").removesuffix("```").strip())
    except Exception as e:
        print("[Warning] LLM response was not valid JSON. Skipping structured metadata.")
        structured_data = {}

    result = {
        "format": "PDF",
        "intent": intent,
        "text_excerpt": text[:1000],  # Limit long docs
        "metadata": structured_data
    }

    memory.update_context(result)
    return result
