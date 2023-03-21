FROM python:3.9

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="$PATH:/root/.local/bin"

CMD ["python3"]
