FROM alpine:latest

RUN apk add python3 py3-flask uwsgi uwsgi-http uwsgi-python3

COPY docroot.html ./
COPY .auth_tokens ./
COPY hook2shell/hook2shell.py ./

CMD ["/usr/sbin/uwsgi", "--plugins", "http,python", "--http", ":9080", "--manage-script-name", "--mount", "/=hook2shell:app"]
