🪝 hook2shell 🐚
================

Very beta. A webhook listener that runs shell commands.

This might be useful on single-user Linux hosts or in tightly controlled environments. I would not recommend running this application on a world-accessible server.

Commands can require authentication tokens. There is an `EXAMPLE.auth_tokens` file, rename this to `.auth_tokens` to test with this file. A sufficiently complex token (say, a SHA256 hash generated from random data) should be sufficiently unguessable (that it, it would take a very long time to brute-force). A future feature could be to lookup tokens from a database, a token administrator admin endpoint, etc. At that point, maybe just use JWT tokens.

Questions:

* Should all routes check for authorization? If so, how to allow for routes that should be "public"?
* Use a decorator for routes that require authorization
* Use a config file instead of constants (see below)
* Can the route/endpoints be normalized? Is that a variable that is already available to Flask? I'm thinking of comparing `route` and `/route` and `/route/` in the `.auth_token` file.

Config options
--------------

Currently in `hook2shell.py`, could be moved to a config file:

    ENFORCE_SHA256_TOKENS=False
    ALLOW_NON_EXPIRING_TOKENS=True
    NON_EXPIRING_SYMBOLS=["*", "-"]


Run in the Flask dev server
---------------------------

    git clone https://github.com/cherdt/hook2shell.git 
    cd hook2shell
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    export FLASK_APP=hook2shell.py
    flask run

Build the Docker container
--------------------------

    docker build --tag hook2shell .

Run in the Docker container
---------------------------

    docker run -d -p 9080:9080 hook2shell

Using with an Apache2 reverse proxy
-----------------------------------

I added the following to my Apache2 config to pass traffic to the uWSGI server running on the Docker container. Note that [mod_proxy](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html) must be enabled:

    ProxyPass "/hook2shell"  "http://localhost:9080/"
    ProxyPassReverse "/hook2shell"  "http://localhost:9080/"

Using with an Nginx reverse proxy
---------------------------------

I added the following to my Nginx config to pass traffic to the uWSGI server running on the Docker container:

    location /hook2shell/ {
        proxy_pass http://localhost:9080/;
    }

Note that Nginx can use the uWSGI protocol directly. I have not tried this, see [uWSGI: Putting behind a full webserver](https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html#putting-behind-a-full-webserver) for details.
