import json
import requests

chat_history = []


def get_bot_response(user_message, language):
    try:
        # Add a system instruction to guide the model's language
        system_instruction = f"All your responses must be in {language}. If you cannot fulfill the request, apologize in {language}."

        # Add the user's message to the chat history
        chat_history.append({"role": "user", "parts": [{"text": user_message}]})

        # IMPORTANT: Hardcoded API key is a security risk. It should be stored as an environment variable.
        #api_key = "AIzaSyDIfuvL8H8N7S9hYwsQYFQsnBSqHeVc1w8"

        api_key="AIzaSyD9QtQq36Z9KYS1R0kTeK06anNu0GckyXs"
        # api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

        model = "gemini-2.5-flash"  # or another model from the docs
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        # Construct the payload with both chat history and the system instruction
        payload = {
            "contents": chat_history,
            "systemInstruction": {
                "parts": [{"text": system_instruction}]
            }
        }

        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status()

        result = response.json()
        bot_text = "I'm sorry, I couldn't generate a response."
        if result and 'candidates' in result and len(result['candidates']) > 0:
            bot_text = result['candidates'][0]['content']['parts'][0]['text']

        # Append the bot's response to the chat history
        chat_history.append({"role": "model", "parts": [{"text": bot_text}]})
        return bot_text

    except Exception as e:
        print(f"Chatbot Error: {e}")
        return "Bot: Error occurred while processing your message."
