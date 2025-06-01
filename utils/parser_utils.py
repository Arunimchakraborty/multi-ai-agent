from utils.llm_utils import query_ollama
import json
import re
import fitz  # PyMuPDF

def detect_format(input_data: bytes | str, filename=None) -> str:
    # Check for PDF magic number
    if filename and filename.lower().endswith(".pdf"):
        return "PDF"
    elif isinstance(input_data, bytes):
        # PDF files start with "%PDF" at beginning in bytes
        if input_data.startswith(b"%PDF"):
            return "PDF"
        # Could add more checks here if needed

    # If input_data is bytes, try to decode to string for LLM
    if isinstance(input_data, bytes):
        try:
            input_text = input_data.decode("utf-8", errors="ignore")
        except:
            input_text = ""
    else:
        input_text = input_data

    prompt = (
        "You are a helpful assistant. Detect the input format. "
        "Answer with exactly one of: PDF, JSON, Email.\n\n"
        f"Input:\n{input_text}\n\nFormat:"
    )
    response = query_ollama(prompt)
    response = response.strip().lower()
    if "json" in response:
        return "JSON"
    elif "email" in response:
        return "Email"
    elif "pdf" in response:
        return "PDF"
    else:
        return "Unknown"


def detect_intent(text: str) -> str:
    prompt = (
    "You are an intelligent document classification assistant trained to analyze and understand various types of business and regulatory documents. "
    "Given the text below, identify the most appropriate intent based on its content. "
    "Choose *only one* from the following intents:\n\n"
    "- Invoice: A financial document confirming payment due, including details like invoice number, date, and amount.\n"
    "- RFQ (Request for Quotation): A formal business request asking for price quotes, service details, or bids—usually involves phrases like 'please provide pricing', 'quotation requested', or 'we are looking for suppliers'.\n"
    "- Complaint: A message expressing dissatisfaction, reporting issues, or requesting a correction—look for words like 'issue', 'problem', 'discrepancy', or 'not satisfied'.\n"
    "- Regulation: An official rule, policy, or legal text, often issued by a governing authority or compliance body—watch for references to 'compliance', 'shall be', 'regulatory authority', 'as per Section X', or similar legalistic tone. Can also contin 'shall', 'must', 'section', 'act', or references to compliance and penalties.\n"
    "- General: Documents that do not contain legal or regulatory language or authority, and do not fit Invoice, RFQ, or Complaint.\n\n"
    "⚠️ Pay close attention to the *purpose* and *tone* of the document:\n"
    "- RFQs are inquiries or solicitations for a service/product from vendors.\n"
    "- Regulations are *rules*, not requests—they often come from authorities and have a declarative/legal tone.\n\n"
    "Do not confuse RFQs with Regulations—RFQs are usually sent by companies *asking* for quotes, while Regulations are *stated* by institutions and impose rules.\n\n"
    "Respond with only one of the following: 'Invoice', 'RFQ', 'Complaint', 'Regulation', or 'General'.\n\n"
    f"Document Text:\n{text}\n\n"
    "Predicted Intent:"
)

    response = query_ollama(prompt)
    response = response.strip().capitalize()
    allowed_intents = ["Invoice", "RFQ", "Complaint", "Regulation", "General"]
    for intent in allowed_intents:
        if intent.lower() in response.lower():
            return intent
    return "General"


def extract_email_info(text: str) -> dict:
    prompt = (
        "You are an intelligent assistant that extracts structured metadata from raw email text. "
        "Given the email content below, extract the following fields if present:\n"
        "- sender (email address or name)\n"
        "- subject\n"
        "- summary: a very brief summary of the email content\n"
        "- date\n\n"
        "Return the result as a JSON object with keys: sender, subject, summary, and date. "
        "Answer only the JSON, don't give any other text.\n\n"
        f"Email Text:\n{text}\n\n"
        "Extracted JSON:"
    )

    response = query_ollama(prompt)

    # Strip Markdown-style code fences and backticks if present
    response = re.sub(r"^```(?:json)?|```$", "", response.strip(), flags=re.MULTILINE).strip()

    try:
        return json.loads(response)
    except Exception as e:
        print("[Error] Failed to parse LLM response as JSON:", response)
        return {"sender": None, "subject": None, "date": None}

def extract_text_from_pdf(pdf_input):
    if isinstance(pdf_input, bytes):
        # Open from bytes buffer
        doc = fitz.open(stream=pdf_input, filetype="pdf")
    else:
        # Assume pdf_input is a path string
        doc = fitz.open(pdf_input)

    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text
