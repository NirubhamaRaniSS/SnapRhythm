import requests
from base64 import b64encode

client_id = "b01a4d1080fa46afb3856d6a21f3580a"
client_secret = "de47ea7ee9a64f10827f42ae6bb0d76a"

auth_str = f"{client_id}:{client_secret}"
b64_auth_str = b64encode(auth_str.encode()).decode()

headers = {
    "Authorization": f"Basic {b64_auth_str}",
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "grant_type": "client_credentials"
}

response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

access_token = response.json().get("access_token")
print("Access Token:", access_token)
