from flask import Flask, render_template, request, redirect, session, flash
from creating_playlist import create_playlist
from add_func import validate_date, generate_random_string, sha256, base64encode
from access_token import get_access_token
import urllib.parse
import requests
import re
import os

app = Flask(__name__)
app.secret_key = "secret_key"

regex_pattern = r'^\d{4}-\d{2}-\d{2}$'

AUTH_URL = "https://accounts.spotify.com/authorize"
NAME_URL = "https://api.spotify.com/v1/me"
TOKEN_URL = "https://accounts.spotify.com/api/token"

user_id = ""
user_name = ""
client_id = os.environ.get("client_id")
redirect_uri = os.environ.get("redirect_uri")
client_secret = os.environ.get("client_secret")
code_verifier = generate_random_string(82)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    hashed = sha256(code_verifier)
    code_challenge = base64encode(hashed)

    params_auth_url = {
        "client_id": client_id,
        "response_type": 'code',
        "redirect_uri": redirect_uri,
        "scope": 'playlist-modify-public playlist-modify-private',
        "code_challenge_method": "S256",
        "code_challenge": code_challenge
    }

    auth_url = f"{AUTH_URL}?" + urllib.parse.urlencode(params_auth_url)
    return redirect(auth_url)


@app.route("/callback")
def callback():
    global user_id, user_name
    code = request.args.get("code")

    if code:
        token_info = get_access_token(code, client_id, client_secret, redirect_uri, code_verifier, TOKEN_URL)

        session["access_token"] = token_info["access_token"]

        headers = {
            "Authorization": f"Bearer {session["access_token"]}"
        }
        name_req = requests.get(url=NAME_URL, headers=headers)
        user_name = name_req.json()["display_name"]
        user_id = name_req.json()["id"]

    return render_template("logged.html", user_name=user_name)


@app.route("/creating", methods=["POST"])
def creating_playlist():
    global user_id, user_name
    date = request.form.get('date')
    token = session["access_token"]

    if re.match(regex_pattern, date) and validate_date(date):
        create_playlist(user_id, date, token)
        return render_template("finished.html")

    else:
        flash("Date is not in correct format or within a given date time range")
        return render_template("logged.html", user_name=user_name)


if __name__ == "__main__":
    app.run(host="localhost", port=5555)
