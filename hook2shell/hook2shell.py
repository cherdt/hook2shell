"""hook2shell: call a webhook, run a shell command"""
import datetime
import subprocess
from flask import Flask, abort
app = Flask(__name__)

ENFORCE_SHA256_TOKENS=False
ALLOW_NON_EXPIRING_TOKENS=True
NON_EXPIRING_SYMBOLS=["*", "-"]

with open('./docroot.html', encoding="utf-8") as f:
    docroot_html = f.read()

with open('.auth_tokens', encoding="utf-8") as f:
    auth_tokens = f.readlines()

def does_not_expire(expiration):
    """Returns True if the expiration field indicates a non-expirinng token"""
    if ALLOW_NON_EXPIRING_TOKENS and expiration in NON_EXPIRING_SYMBOLS:
        return True
    return False

def is_future_date(expiration):
    """Returns True if today is strictly less than the expiration date"""
    try:
        (year, month, day) = expiration.split("-")
        if datetime.date.today() < datetime.date(int(year), int(month), int(day)):
            return True
        return False
    except:
        return False

def is_valid_expiration(expiration):
    """Returns True if:
       - expiration is in the future
       - expiration is a symbol indicating non-expiring symbols AND
       - non-expiring symbols are allowed"""
    if is_future_date(expiration):
        return True
    if does_not_expire(expiration):
        return True
    return False

def is_valid_auth_token(endpoint, token):
    """Check the user-supplied token agains auth_tokens"""
    for line in auth_tokens:
        if line.startswith("#"):
            continue
        else:
            (path, expiration, secret) = line.rstrip().split('\t')
            if not is_valid_expiration(expiration):
                continue
            if ENFORCE_SHA256_TOKENS and not (len(secret) == 64 and secret.isalnum()):
                continue
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
        abort(401)

    output = subprocess.check_output(['ls', '-l'])
    return f"ran ls: {output}"

@app.route("/generate")
def generate():
    """An endpoint that generates a SHA256sum from /dev/urandom"""
    output = subprocess.getoutput(
            ['head /dev/urandom | sha256sum | cut -d" " -f1'])
    return f"New token: {output}"

@app.route("/test/")
def test():
    """A test endpoint that does not require a token"""
    return "this is a test"


@app.route("/")
def docroot():
    """Display a basic web page"""
    return docroot_html
