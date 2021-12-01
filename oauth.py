import requests
from config import OAUTH_URL

def verify(token):
    url = OAUTH_URL+token
    try:
        res = requests.get(url)
        if res.status_code!=200:
            return None
        data = res.json()
        if data.get("isAuthed"):
            return res.json()
        else:
            return None
    except Exception as e:
        return None
