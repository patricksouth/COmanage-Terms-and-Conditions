# COmanage Terms and Conditions Demo

A lightweight Flask web application that authenticates users via OpenID Connect (OIDC) and displays decoded ID token claims in a formatted web interface.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Skiddler233/COmanage-Terms-and-Conditions.git
cd COmanage-Terms-and-Conditions
````

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# or
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env file, using .env_default as a template
```bash
PYTHON_VER=3.14 # Increment with newer releases

APP_SESSION_SECRET=<value> # 32 char random string

CLIENT_ID=<client_id>
CLIENT_SECRET=<client_secret>
REDIRECT_URI=http://localhost/authenticate # Matches the redirect URI registered with the OIDC OP.

TOKEN_ENDPOINT=https://<OIDC_OP_URL>/oauth2/token
DISCOVERY_URL=https://<OIDC_OP_URL>/.well-known/openid-configuration

```
Update the .env file replacing <values> with suitable values.

PYTHON_VER: Select a suitable "slim" Python image "version" from https://hub.docker.com/_/python/tags?name=slim - only used by Docker

APP_SESSION_SECRET: A random string used by Flask for session encryption.

CLIENT_ID: Client ID when registering the application with the OIDC provider.

CLIENT_SECRET: Client secret when registering the application with the OIDC provider.

REDIRECT_URI: Matches the redirect URI registered with the OIDC OP.

TOKEN_ENDPOINT: From OIDC OP .well-known/openid-configuration

DISCOVERY_URL: OIDC OP .well-known/openid-configuration

## To run as a Dockerise flask app
After adding details to .env file.

To start container
```
make up
```

The Flask app logs to console, press CTRL+C to quit.

To stop container
```
make down
```
