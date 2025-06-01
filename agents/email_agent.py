from utils.parser_utils import extract_email_info


def process_email(email_text: str, memory):
    info = extract_email_info(email_text)
    memory.update_context(info)
    return {"status": "processed", "data": info}
