"""
One-time local setup — run this on a machine with a browser:

    python gmail_auth_setup.py

It opens a Google consent screen for anushkadevg@gmail.com. After you click
Allow, it writes token.json next to this file. Copy that token.json to the
server as part of deployment — the server (routes.py) only ever reads
token.json and never needs this script or a browser.

Your OAuth client is a "Web application" type with redirect URI
http://127.0.0.1:8000 registered, so:
  1. Stop uvicorn first (this script needs port 8000 free).
  2. Run this script — it opens your browser to Google's consent screen.
  3. After you approve, restart uvicorn normally.

Re-run this script only if token.json is deleted/revoked or the scope changes.
"""
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
CLIENT_SECRET_FILE = "client_secret_411398889334-4bcpl6cam3knkdedfg9t57l5p81c48gk.apps.googleusercontent.com.json"
TOKEN_FILE = "token.json"

if __name__ == "__main__":
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=8000)
    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())
    print(f"Saved {TOKEN_FILE} — deploy this file to the server alongside the app.")
