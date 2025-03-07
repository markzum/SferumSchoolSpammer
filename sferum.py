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


def send_message_with_image(message, image_url):
    access_token = get_auth_token()

    url = "https://api.vk.me/method/photos.getMessagesUploadServer?v=5.246"
    resp = requests.post(url, data={
        "access_token": access_token,
        "group_id": 0,
        "upload_v2": 1,
        "lang": "ru"
    })
    upload_url = resp.json()['response']['upload_url']

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    image_data = requests.get(image_url, headers=headers).content
    # print(image_data)
    files = {
        'file1': ('image.jpg', image_data, 'image/jpeg')
    }
    resp = requests.post(upload_url, files=files)

    url = "https://api.vk.me/method/photos.saveMessagesPhoto?v=5.246"
    resp = requests.post(url, data={
        "access_token": access_token,
        "upload_v2": 1,
        "photo": resp.text,
        "group_id": 0,
        "lang": "ru"
    })
    photo_id = resp.json()['response'][0]['id']

    attachment = f"photo{config.SFERUM_USER_ID}_{photo_id}"


    url = "https://api.vk.me/method/messages.send?v=5.245"

    data = {
        "access_token": access_token,
        "peer_id": config.SFERUM_DESTINATION_PEER_ID,
        "random_id": -random.randint(1, 10000000),
        "message": message,
        "attachment": attachment,
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
    # print(send_message("Привет! Это тест!"))
    print(send_message_with_image("Привет! Это тест!", "https://upload.wikimedia.org/wikipedia/commons/7/73/Pacific_bluefin_tuna.jpg"))
    # print(get_auth_token())

