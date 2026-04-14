import requests

# def get_ai_response(text, model="llama3"):
def get_ai_response(text, model="phi3"):
    import requests

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": text,
        "stream": False
    }

    r = requests.post(url, json=payload)
    return r.json()["response"]