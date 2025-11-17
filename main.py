import os
import uuid
import json
import requests
import dotenv
from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt, JsonWebKey

app = Flask(__name__)
dotenv.load_dotenv()
app.secret_key = os.getenv('APP_SESSION_SECRET')

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT")
DISCOVERY_URL = os.getenv("DISCOVERY_URL")
TERMS_URL = os.getenv("TERMS_URL")

oauth = OAuth(app)

oidc = oauth.register(
    name="oidc",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=DISCOVERY_URL,
    token_endpoint=TOKEN_ENDPOINT,
    client_kwargs={
        'scope': 'openid profile email org.cilogon.userinfo',
        'response_mode': 'jwt'
    }
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    nonce = str(uuid.uuid4())
    session['nonce'] = nonce
    return oidc.authorize_redirect(REDIRECT_URI, nonce=nonce)

def decode_id_token(id_token, jwks_uri):
    jwks = requests.get(jwks_uri).json()
    key_set = JsonWebKey.import_key_set(jwks)
    claims = jwt.decode(id_token, key_set)
    claims.validate()
    return dict(claims)

@app.route('/authenticate')
def authenticate():
    token = oidc.authorize_access_token()
    nonce = session.get('nonce')
    if not nonce:
        return "Missing nonce in session", 401
    session.pop('nonce')

    oidc.parse_id_token(token, nonce=nonce)
    id_token = token['id_token']
    jwks_uri = oidc.server_metadata['jwks_uri']
    decoded_token = decode_id_token(id_token, jwks_uri)

    session['user'] = decoded_token

    # Terms check logic
    terms = decoded_token.get('terms_and_conditions', [])
    for item in terms:
        if item.get('name') == 'GUARDIANS Acceptable Use Policy':
            if not item.get('agreed', False):
                return redirect(url_for('terms'))
            break

    return redirect(url_for('token_view'))

@app.route('/terms')
def terms():
    user = session.get('user', {})
    name = user.get('given_name', 'User')
    try:
        response = requests.get(TERMS_URL, timeout=10)
        response.raise_for_status()
        terms_html = response.text
    except requests.exceptions.RequestException as e:
        terms_html = f"<p>Unable to load Terms and Conditions: {e}</p>"

    return render_template("terms.html", name=name, terms_html=terms_html)

@app.route('/terms/accept', methods=['POST'])
def accept_terms():
    user = session.get('user', {})
    user['terms_and_conditions'] = [{'name': 'GUARDIANS Acceptable Use Policy', 'agreed': True}]
    session['user'] = user
    return redirect(url_for('terms_success'))

@app.route('/terms/success')
def terms_success():
    user = session.get('user', {})
    name = user.get('given_name', 'User')
    return render_template('terms_success.html', name=name)

@app.route('/token_view')
def token_view():
    decoded_token = session.get('user')
    if not decoded_token:
        return "No token found in session", 401
    return render_template('token_view.html', token=decoded_token)

if __name__ == '__main__':
    app.run(debug=True)
