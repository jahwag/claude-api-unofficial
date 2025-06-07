#!/usr/bin/env python3
"""
Minimal OAuth 2.0 PKCE demo for Claude Code API
Logs in and displays user profile as verification
"""
import base64
import hashlib
import http.server
import secrets
import socketserver
import threading
import urllib.parse
import webbrowser
from urllib.request import Request, urlopen
import json

# OAuth config
CLIENT_ID = "9d1c250a-e61b-44d9-88ed-5944d1962f5e"
REDIRECT_URI = "http://localhost:54545/callback"
SCOPES = "org:create_api_key user:profile user:inference"

# Global to store auth code and state
auth_code = None
auth_state = None
server_running = True

def generate_pkce():
    """Generate PKCE code verifier and challenge"""
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    return code_verifier, code_challenge

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code, auth_state, server_running
        if self.path.startswith('/callback'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            if 'code' in params and 'state' in params:
                if params['state'][0] == auth_state:
                    auth_code = params['code'][0]
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'<h1>Success!</h1><p>You can close this window.</p>')
                    server_running = False
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'State mismatch error')
            else:
                self.send_response(400)
                self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Silence server logs

def start_callback_server():
    """Start callback server"""
    with socketserver.TCPServer(("", 54545), CallbackHandler) as httpd:
        while server_running:
            httpd.handle_request()

def exchange_code_for_tokens(code, code_verifier, state):
    """Exchange authorization code for tokens"""
    data = json.dumps({
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'code_verifier': code_verifier,
        'state': state
    }).encode()
    
    req = Request('https://console.anthropic.com/v1/oauth/token', data=data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json, text/plain, */*')
    req.add_header('User-Agent', 'oauth-demo/1.0')
    
    with urlopen(req) as response:
        return json.loads(response.read())

def get_user_profile(access_token):
    """Fetch user profile"""
    req = Request('https://api.anthropic.com/api/oauth/profile')
    req.add_header('Authorization', f'Bearer {access_token}')
    req.add_header('Accept', 'application/json, text/plain, */*')
    req.add_header('User-Agent', 'oauth-demo/1.0')
    
    with urlopen(req) as response:
        return json.loads(response.read())

def main():
    global auth_code, auth_state
    
    print("Starting OAuth 2.0 PKCE flow...")
    
    # Generate PKCE and state
    code_verifier, code_challenge = generate_pkce()
    auth_state = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    
    # Build authorization URL
    auth_url = f"https://claude.ai/oauth/authorize?" + urllib.parse.urlencode({
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
        'state': auth_state
    })
    
    # Start callback server
    server_thread = threading.Thread(target=start_callback_server, daemon=True)
    server_thread.start()
    
    print(f"Opening browser: {auth_url}")
    webbrowser.open(auth_url)
    
    # Wait for callback
    print("Waiting for authorization...")
    server_thread.join()
    
    if not auth_code:
        print("Error: No authorization code received")
        return
    
    try:
        # Exchange code for tokens
        print("Exchanging code for tokens...")
        tokens = exchange_code_for_tokens(auth_code, code_verifier, auth_state)
        
        # Get user profile
        print("Fetching user profile...")
        profile = get_user_profile(tokens['access_token'])
        
        print(f"\n✓ Login successful!")
        print(f"User: {profile['account'].get('display_name', 'Unknown')}")
        print(f"Email: {profile['account'].get('email', 'Unknown')}")
        print(f"Organization: {profile['organization'].get('name', 'Unknown')}")
        print(f"Access token: {tokens['access_token'][:20]}...")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()