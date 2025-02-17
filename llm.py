import requests
import config
import random


def _get_random_word():
    files = ['animals.txt', 'birds.txt']
    words = []
    for file in files:
        with open(f"dicts/{file}", 'r', encoding='utf-8') as f:
            words += f.readlines()
    
    return random.choice(words).strip()


def _make_request(messages):
    url = "https://api.edenai.run/v2/multimodal/chat"

    payload = {
        "response_as_dict": False,
        "temperature": 0.5,
        "max_tokens": 1000,
        "messages": messages,
        "providers": "openai/gpt-4o-mini"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {config.EDENAI_TOKEN}",
        "Referer": "https://app.edenai.run/"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def generate_story():
    response = _make_request([
        {"role": "user", "content": [{"type": "text", "content": {"text": "Ты - писатель. Напиши неболшую, но захватывающую историю про то слово, которое тебе я тебе сейчас напишу. Слово: " + _get_random_word()}}]}
    ])
    if 'error' in response:
        raise Exception(response['error'])
    return response[0]['generated_text']


if __name__ == "__main__":
    print(generate_story())

