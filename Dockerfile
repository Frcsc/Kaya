FROM python:3.10

WORKDIR /kaya

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv sync --system --dev

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
