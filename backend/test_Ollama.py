import requests
import json

url = "http://192.168.1.11:11434/api/generate"
data = {
    "model": "llama3.2",  # ou ton modèle installé
    "prompt": "Dis bonjour en français",
    "stream": False
}

response = requests.post(url, json=data)
print(response.json()["response"])