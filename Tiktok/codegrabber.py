from flask import Flask, request
import webbrowser
import os

app = Flask(__name__)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    print(f"Authorization code: {code}")
    return "Authorization successful! You can close this window."

if __name__ == '__main__':
    # Open the authorization URL in the default web browser
    import secrets

    client_id = os.getenv("Tiktok Client")
    redirect_uri = 'http://localhost:5000/callback'
    scopes = 'user.info.basic+video.upload'
    state = secrets.token_urlsafe(16)

    auth_url = (
        f"https://open-api.tiktok.com/platform/oauth/connect/"
        f"?client_key={client_id}&response_type=code&scope={scopes}"
        f"&redirect_uri={redirect_uri}&state={state}"
    )

    app.run(port=5000)
    webbrowser.open(auth_url)  # Automatically opens the URL in the default browser