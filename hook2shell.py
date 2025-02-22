"""hook2shell: call a webhook, run a shell command"""
import subprocess
from flask import Flask
app = Flask(__name__)

ENFORCE_SHA256_TOKENS=False

with open('./docroot.html', encoding="utf-8") as f:
    docroot_html = f.read()

with open('.auth_tokens', encoding="utf-8") as f:
    auth_tokens = f.readlines()

def is_valid_auth_token(endpoint, token):
    """Check the user-supplied token agains auth_tokens"""
    for line in auth_tokens:
        if line.startswith("#"):
            continue
        # TODO: check for valid date
        else:
            (path, exp, secret) = line.rstrip().split('\t')
            if ENFORCE_SHA256_TOKENS and not (len(secret) == 64 and secret.isalnum()):
                return False
            if endpoint == path and token == secret:
                return True
    return False

def is_authorized(endpoint, token):
    """Check if the token is authorized to access the specified endpoint"""
    # hard-coded example
    if endpoint == "ls" and token == "token":
        return True

    return is_valid_auth_token(endpoint, token)


@app.route("/ls/")
def ls_token():
    """This endpoint requires a token"""
    return "This endpoint requires an auth token"


@app.route("/ls/<token>")
def get_ls(token):
    """Run the ls command"""
    if not is_authorized("ls", token):
        return f"not authorized: {token}"

    output = subprocess.check_output(['ls', '-l'])
    return f"ran ls: {output}"

@app.route("/generate")
def generate():
    """An endpoint that generates a SHA256sum from /dev/urandom"""
    output = subprocess.getoutput(['head /dev/urandom | sha256sum'])
    return f"New token: {output}"

@app.route("/test/")
def test():
    """A test endpoint that does not require a token"""
    return "this is a test"


@app.route("/")
def docroot():
    """Display a basic web page"""
    return docroot_html
