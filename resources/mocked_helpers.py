import requests


def get_user_profile() -> dict:
    url = "https://randomuser.me/api"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        return {}