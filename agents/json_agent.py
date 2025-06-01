import json

def process_json(json_data, memory):
    
    expected_keys = {"invoice_number", "date", "amount", "recipient"}  # example
    
    missing = expected_keys - json_data.keys()
    expected_keys = {"invoice_id", "amount", "date", "sender"}
    missing = expected_keys - json_data.keys()
    result = {
        "valid": not missing,
        "missing_fields": list(missing),
        "data": json_data
    }
    memory.update_context(result)
    return result
