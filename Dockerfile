FROM python:3.11.4

ENV PATH="/root/.local/bin:$PATH"

COPY ./poetry.lock /
COPY ./pyproject.toml /


RUN apt-get update -y && apt-get install -y curl \
&& curl -sSL https://install.python-poetry.org | python3 - \
&& poetry install \
&& apt-get remove curl -y \

COPY . .
WORKDIR .
