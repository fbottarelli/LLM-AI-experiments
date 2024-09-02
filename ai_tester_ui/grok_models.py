import requests
import json

api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

# print pretty
print(json.dumps(response.json(), indent=4))
# print all id
for model in response.json()['data']:
    print(model['id'])