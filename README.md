hook2shell
==========

A webhook listener that runs shell commands.

Commands can require authorization. There is an `EXAMPLE.auth_tokens` file, rename this to `.auth_tokens` to test with this file.

Questions:

* Should all routes check for authorization? If so, how to allow for routes that should be "public"?
* What should a non-expiring token look like? `*`? `-`? Anything that is not a valid date?
* My example uses a SHA256 hash value for a token, but tokens can be anything. Should that be restricted? Force people to use non-trivial tokens?

Other questions:

* Can the route/endpoints be normalized? Is that a variable that is already available?
* if the route is `route` can `route/` also work? Should it also work?


TODO:
-----

Respect token/secret expirations.

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

