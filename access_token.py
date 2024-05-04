import requests


def get_access_token(code, client_id, client_secret, redirect_uri, code_verifier, TOKEN_URL):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
        "code_verifier": code_verifier,
    }
    response = requests.post(TOKEN_URL, data=data)
    token_info = response.json()
    return token_info
