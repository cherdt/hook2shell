hook2shell
==========

A webhook listener that runs shell commands.

TODO:
-----

Actually make use of tokens/secrets in some way.

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

