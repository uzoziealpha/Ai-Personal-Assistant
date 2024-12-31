import requests

# Replace with your DeepSeek API key
DEEPSEEK_API_KEY = "sk-7df095967fcd40fb9942443e2d9fadce"

# DeepSeek API endpoint (replace with the actual endpoint)
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Example endpoint

def call_deepseek_api(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",  # Replace with the correct model name
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Test the DeepSeek API
response = call_deepseek_api("Write a haiku about AI")
print(response)