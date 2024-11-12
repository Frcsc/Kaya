# Kaya Django Server

This is a python based application that is intended to expose API endpoints for kaya. Django and Django REST framework (DRF) were used for this task. Django provides a custom command setup that can be extended to run custom commands and DRF is is a powerful and flexible toolkit for building APIs.

## Application Setup

Copy the contents of `dev-example.env` and past them in a new file called `.env` in the root directory. The root directory is where `Pipfile.lock` and `Pipfile` are located.

## Build and run the application with Docker or Native

First, make sure you are in the root directory.

### Docker Development Quick Start

This mode requires the following dependencies, so first install them on your system using your preferred method.

- Docker
- Docker compose

1. Build Docker Image

```
docker compose build
```

2. Apply database migrations

```
docker compose run django python manage.py migrate
```

3. Add seed data to the database

```
docker compose run django python manage.py seed_db
```

4. Star docker container (Note: django dev server will use port 8000 by default)

```
docker compose up
```

### Native Development Quick Start

This mode requires the following dependencies, so first install them on your system using your preferred method.

- Python 3.10
- Pipenv
- PostgreSQL 14 or compatible

1. Set up the Python virtual environment, and download and install all the Python dependencies

```
pipenv sync
```

2. Apply database migrations

```
pipenv run ./manage.py migrate
```

3. Add seed data to the database

```
pipenv run ./manage.py seed_db
```

4. Start development server (Note: django dev server will use port 8000 by default)

```
pipenv run ./manage.py runserver
```

### Pre-commit setup (Optional but highly recommended. The CI/CD will run it when PRs are made or when changes are pushed to a branch that runs Github actions)

Developers should run `pre-commit run --all-files` to check their code quality before pushing any changes to the repo.

1. Install pre-commit

```pip install pre-commit
```

2. Setup pre-commit in git repo

```
pre-commit install
```

3. Run pre-commit in all file

```
pre-commit run --all-files
```

## Assumptions

- The data provided in the dataset can be used for database seeding.

## Solution Explanations / steps

### Databse

The data source provided was used to form the bases of Database table construction. Using Django's ORM three models where created.

- Campaign fields: `campaign_id, campaign_name, campaign_type` . These fields also represents colums in the postgres database

- AdGroup fields: `ad_group_id, ad_group_name, campaign(ForeignKey)`.

- AdGroupStat : `date, ad_group(ForeignKey), device, impressions, clicks, conversions, cost`.


### API endpoints

- Here are the 4 API endpoints, in order to access them the development server must be up and running.

  - List of campaigns

    ```
    http://localhost:8000/api/campaign/v1/campaigns
    ```

  - Patch campaign name. Assume `21358147155` is a valid campaign_id.

    ```
    http://localhost:8000/api/campaign/v1/campaign/21358147155
    ```

  - Get performance time-series data.

    ```
    http://localhost:8000/api/ad-group-stats/v1/performance-time-series
    ```

  - Get Performance comparison data.

    ```
    hhttp://localhost:8000/api/ad-group-stats/v1/compare-performance
    ```

- Four key API endpoints were build as specified on the assignment page. Key adjust(s).

  - `POST /update-campaign` was changed to `Patch /campaign/<campaign_id>`. Patch is more standard for changing a single value of an instance. The name change is also more representative and for data changes, `update-campaign` is very discriptive which is not a good security practice in most cases. Finally, the API can simply be extend if there's a need for other API actions like `delete and retrieve`

  - The API endpoints can be found in the project apps they belong to in a file called `api.py`.

  - Every API has permissions. Currently the permissions are `public`. If there's a need for a user to be authenticatied and authorized to acess any API endpoint, the APIs can be easily adjusted.

  - A version number was added to all the API paths. This is beneficial to track future application version changes. It could also be beneficial on a production, where we may need to run two different versions of the same API for different client application applications.

  - A new app was added to manage potential user setup. A `register` and `login` APIs have be added as well.

### Unit Test

About 21 unit tests were added to over every aspect of the key API endpoints. Factory-boy (refer to refrences) library was used to generate random instances for test cases.

- Run all test cases with `Native development`

```
pipenv run ./manage.py test
```

`OR`

- Run all test cases with with `Docker development`

```
docker compose run django python manage.py test
```

### Admin Dashboard Web page

Django comes with an inbuilt dashboard. You can create an admin user and navigate to `http://0.0.0.0:8000/admin` to view all the seed data on a dashboard.

Create an admin user with the command below and answer the prompt questions (`email, password`) and proceed to the login on the admin page (`http://0.0.0.0:8000/admin`)

- Create admin user with `Native development`

```
pipenv run ./manage.py createsuperuser
```

`OR`

- Create admin user with `Docker development`

```
docker compose run django python manage.py createsuperuser
```

## Reference

- [Pre-commit](https://pre-commit.com/#install)
- [Django Rest Framework filter](https://django-filter.readthedocs.io/en/stable/)
- [Factory-boy](https://factoryboy.readthedocs.io/en/stable/orms.html)
- [watch tower](https://pypi.org/project/watchtower/)
