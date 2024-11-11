FROM python:3.10-slim

WORKDIR /kaya

RUN pip install --upgrade pip

COPY Pipfile Pipfile.lock /kaya/
COPY . /kaya

RUN pip install pipenv
RUN pipenv sync --system

COPY entrypoint.sh /kaya/
RUN chmod +x /kaya/entrypoint.sh

EXPOSE 8000

CMD ["/kaya/entrypoint.sh"]
