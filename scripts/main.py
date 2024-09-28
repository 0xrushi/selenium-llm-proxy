from flask import Flask, request, jsonify
import os
from functools import wraps
import requests
import uuid
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from dotenv import load_dotenv
load_dotenv()

from selenium_automator import ask_gpt_for_final_answer, gptParser

app = Flask(__name__)

def send_text(messages: list, model: str = "gpt-3.5-turbo") -> dict:
    """
    Sends a request to the OpenAI API with the provided messages and model.

    Args:
        messages (list): A list of messages to send to the model.
        model (str): The model to use for the request (default is "gpt-3.5-turbo").

    Raises:
        ValueError: If the OPENAI_API_KEY environment variable is not set.

    Returns:
        dict: The JSON response from the OpenAI API.
    """
    if not isinstance(messages, list):
        raise TypeError("messages must be a list")
    if not isinstance(model, str):
        raise TypeError("model must be a string")
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    return response.json()

def send_text_hardcoded(messages: list, model: str = "gpt-3.5-turbo") -> dict:
    """
    Generates a hardcoded response in the format expected from the OpenAI API.

    Args:
        messages (list): A list of messages (not used in this function).
        model (str): The model to use for the response (default is "gpt-3.5-turbo").

    Returns:
        dict: A mock response simulating the OpenAI API response.
    """
    if not isinstance(messages, list):
        raise TypeError("messages must be a list")
    if not isinstance(model, str):
        raise TypeError("model must be a string")
    
    # Hardcoded response in OpenAI format
    hardcoded_response = "This is a hardcoded response from the mock OpenAI API."
    
    return {
        "id": f"chatcmpl-{uuid.uuid4()}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": len(hardcoded_response.split()),
            "total_tokens": 10 + len(hardcoded_response.split())
        },
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": hardcoded_response
                },
                "finish_reason": "stop",
                "index": 0
            }
        ]
    }


FAKE_API_KEY = "sk-fake-key-12345"
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if api_key and api_key.startswith('Bearer '):
            api_key = api_key.split('Bearer ')[1]
        if api_key != FAKE_API_KEY:
            return jsonify({"error": "Invalid API key"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/v1/chat/completions', methods=['POST'])
@require_api_key
def chat_completions():
    try:
        logger.info("Received request for chat completions")
        logger.debug(f"Request headers: {request.headers}")
        logger.debug(f"Request data: {request.get_data(as_text=True)}")
        
        data = request.json
        if not data:
            logger.error("No JSON data provided in the request")
            return jsonify({"error": "No JSON data provided"}), 400
        
        messages = data.get('messages')
        if not messages:
            logger.error("No messages found in the request")
            return jsonify({"error": "No messages found in the request"}), 400
        
        model = data.get('model', 'gpt-3.5-turbo')
        
        # response = send_text_hardcoded(messages, model)
        response = ask_gpt_for_final_answer(gpt_parser, str(messages))
        logger.info("Sending hardcoded response")
        logger.debug(f"Response: {response}")
        
        return jsonify(response)
    
    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")
        return jsonify({"error": "An internal server error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    driver = gptParser.get_driver()
    global gpt_parser
    gpt_parser = gptParser(driver)
    app.run(debug=True, port=5000)