# Kaya Django Server

This is a Python-based application intended to expose API endpoints for Kaya. Django and Django REST Framework (DRF) were used for this task. Django provides a setup for custom commands that can be extended to run various tasks, and DRF is a powerful and flexible toolkit for building APIs.

## Application Setup

Copy the contents of `dev-example.env` and paste them in a new file called `.env` in the root directory. The root directory is where `Pipfile.lock` and `Pipfile` are located.

## Build and Run the Application with Docker or Natively

First, make sure you are in the root directory.

### Docker Development Quick Start

This mode requires the following dependencies, so first install them on your system using your preferred method.

- Docker
- Docker compose

1. Build Docker Image:

```
docker compose build
```

2. Apply database migrations:

```
docker compose run django python manage.py migrate
```

3. Add seed data to the database:

```
docker compose run django python manage.py seed_db
```

4. Star docker container (Note: django dev server will use port 8000 by default):

```
docker compose up
```

### Native Development Quick Start

This mode requires the following dependencies, so first install them on your system using your preferred method.

- Python 3.10
- Pipenv
- PostgreSQL 14 or compatible

1. Set up the Python virtual environment, and download and install all the Python dependencies:

```
pipenv sync
```

2. Apply database migrations:

```
pipenv run ./manage.py migrate
```

3. Add seed data to the database:

```
pipenv run ./manage.py seed_db
```

4. Start development server (Note: django dev server will use port 8000 by default):

```
pipenv run ./manage.py runserver
```

### Pre-commit Setup (Optional but Recommended)

It’s recommended to run `pre-commit run --all-files` to check code quality before pushing any changes to the repo.
CI/CD will also run it on pull requests or changes pushed to branches with GitHub Actions enabled.

1. Install pre-commit:

```
pip install pre-commit
```

2. Setup pre-commit in git repo:

```
pre-commit install
```

3. Run pre-commit in all file:

```
pre-commit run --all-files
```

## Assumptions

- The dataset provided can be used for database seeding.

## Solution Explanations / Steps

### Databse

The provided data source was used as the basis for database table construction. Using Django's ORM, three models were created:

- Campaign Model (Table):
  - campaign_id (chars, primary_key)
  - campaign_name (chars)
  - campaign_type (chars, choices=[SEARCH_STANDARD, VIDEO_RESPONSIVE])

- AdGroup Model (Table):
  - ad_group_id (chars, primary_key)
  - ad_group_name (chars)
  - campaign(ForeignKey to `Campaign`)

- AdGroupStat Model (Table):
  - date (datetime)
  - ad_group(ForeignKey to `AdGroup`)
  - device (chars, choices=[MOBILE, TABLET, DESKTOP])
  - impressions (int)
  - clicks (int)
  - conversions (decimal)
  - cost (decimal)

### API Endpoints

Here are the 4 API endpoints. To access them, the development server must be running.

- List of campaigns:

  ```
  http://0.0.0.0:8000/api/campaign/v1/campaigns
  ```

- Patch campaign name (assuming 21358147155 is a valid campaign ID):

  ```
  http://0.0.0.0:8000/api/campaign/v1/campaign/21358147155
  ```

- Get performance time-series data:

  ```
  http://0.0.0.0:8000/api/ad-group-stats/v1/performance-time-series
  ```

- Get performance comparison data:

  ```
  http://0.0.0.0:8000/api/ad-group-stats/v1/compare-performance
  ```

Key API development features and considerations.

- `POST /update-campaign` was changed to `PATCH /campaign/<campaign_id>`. `PATCH` is more standard for updating a single field, and the name change is more descriptive while enhancing security. This endpoint can also be extended for other actions like `DELETE` or `RETRIEVE`.

- API endpoints are organized within the respective project apps in a file called `api.py`.

- All API endpoints have permissions set to `public`. If future endpoints require authentication, adjustments can be made to secure them.

- A version number (`v1`) is added to all API paths to facilitate tracking future API version changes. This approach may be beneficial in production, especially if different clients need different versions of the same API.

- A new app was added to manage user setup, including `register` and `login` API endpoints.

### Unit Testing

Approximately 21 unit tests cover key API endpoints. The factory-boy library (see References) was used to generate random instances for test cases.

- Run all test cases with Docker:

```
docker compose run django python manage.py test
```

- Run all test cases natively:

```
pipenv run ./manage.py test
```

### Admin Dashboard

Django includes an inbuilt admin dashboard. You can create an admin user and access it at `http://0.0.0.0:8000/admin` to view all seeded data.

Create an admin user with the following command, then proceed to the admin page at `http://0.0.0.0:8000/admin`:

- Create an admin user with Docker:

```
docker compose run django python manage.py createsuperuser
```

- Create an admin user natively:

```
pipenv run ./manage.py createsuperuser
```


## Reference

- [Pre-commit](https://pre-commit.com/#install)
- [Django Rest Framework filter](https://django-filter.readthedocs.io/en/stable/)
- [Factory-boy](https://factoryboy.readthedocs.io/en/stable/orms.html)
- [watch tower](https://pypi.org/project/watchtower/)
