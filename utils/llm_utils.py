import requests
import json

def query_ollama(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma3:1b",
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.2,
        "stream": True  # request streaming response
    }

    response = requests.post(url, json=payload, stream=True)
    response.raise_for_status()

    collected_text = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode('utf-8'))
                chunk = data.get("response", "")
                collected_text += chunk

                if data.get("done", False):
                    break
            except json.JSONDecodeError:
                # ignore lines that aren't valid JSON
                continue

    return collected_text.strip()
