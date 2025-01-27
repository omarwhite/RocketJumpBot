import requests
import os

client_id = os.getenv("Tiktok Client")
client_secret = os.getenv("Tiktok Secret")
redirect_uri = 'https://www.tiktok.com/'
code = 'authorization_code'

response = requests.post(
    'https://open-api.tiktok.com/oauth/access_token/',
    data={
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
    }
)
access_token = response.json()['data']['access_token']
