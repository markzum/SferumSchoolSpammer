import requests
import config
import random


def get_auth_token():
    url = "https://web.vk.me/?act=web_token&app_id=8202606&v=5.245"

    headers = {
        "Cookie": f"remixdsid={config.SFERUM_REMIXDSID};"
    }

    resp = requests.post(url, headers=headers)
    resp = resp.json()
    if 'error' in resp:
        print(resp)
        raise Exception("Error while getting auth token!")
    
    for user in resp:
        if user['user_id'] == config.SFERUM_USER_ID:
            return user['access_token']

    return None


def send_message(message):
    url = "https://api.vk.me/method/messages.send?v=5.245"

    data = {
        "access_token": get_auth_token(),
        "peer_id": config.SFERUM_DESTINATION_PEER_ID,
        "random_id": -random.randint(1, 10000000),
        "message": message,
        "entrypoint": "list_all",
        "group_id": 0,
        "lang": "ru"
    }

    resp = requests.post(url, data=data)
    resp = resp.json()
    if 'error' in resp:
        print(resp)
        raise Exception("Error while sending message!")
    return resp


if __name__ == '__main__':
    print(send_message("Привет! Это тест!"))
    # print(get_auth_token())

