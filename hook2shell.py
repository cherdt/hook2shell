"""hook2shell: call a webhook, run a shell command"""
import subprocess
from flask import Flask
app = Flask(__name__)

with open('./docroot.html', encoding="utf-8") as f:
    docroot_html = f.read()


def is_authorized(endpoint, token):
    """Check if the token is authorized to access the specified endpoint"""
    if endpoint == "ls" and token == "token":
        return True
    return False


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


@app.route("/test/")
def test():
    """A test endpoint that does not require a token"""
    return "this is a test"


@app.route("/")
def docroot():
    """Display a basic web page"""
    return docroot_html
