import requests
import logging
from typing import Any, List, Optional, Dict

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SimpleCustomLLM:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def __call__(self, prompt: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        logger.debug(f"Sending request to custom LLM. Headers: {headers}, Data: {data}")
        
        try:
            response = requests.post(f"{self.api_url}/v1/chat/completions", json=data, headers=headers)
            logger.debug(f"Received response. Status code: {response.status_code}, Content: {response.text}")
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in CustomLLM request: {str(e)}")
            raise

llm = SimpleCustomLLM(api_url="http://127.0.0.1:5000", api_key="sk-fake-key-12345")

prompt = "What is a good name for a company that makes eco-friendly water bottles?"

result = llm(prompt)
print(result)