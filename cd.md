# CD

There's a `.github/workflows` folder in the root directory. The folder contains `ci.yml and cd.yml` files used for integration and testing respectively.
These two files are chained as `cd.yml` depends on the successful completion of `ci.yml`

Here is a breakdown of key points in the `cd.yml` file.

## Workflow Triggers

- `on: push:` This workflow is triggered by pushes to the main branch.
- `on: workflow_run:` It also triggers when the Code Quality Tests workflow completes successfully. This chaining ensures that the build and deploy workflow only runs after all tests and code quality checks are passed.

## Environment Variables

- `AWS_REGION`: Specifies the AWS region for deployment (set to `ap-southeast-1`). It’s recommended to move this to AWS secrets if the region might change.
- `IMAGE_NAME`: Defines the name of the Docker image to be built and pushed to Amazon ECR.

## Permissions

`permissions: contents: read:` Provides the workflow read access to the contents of the repository.

## Jobs

### ci Job

This job runs a separate, pre-defined workflow stored in `.github/workflows/ci.yml`, which likely contains additional CI steps. Using `secrets: inherit` allows it to access any secrets defined for the repository.

### deploy Job

- `runs-on: ubuntu-latest`: Specifies the environment to run this job.
- `needs: ci:` This makes the `deploy` job dependent on the `ci` job, meaning it won’t start until ci completes successfully.

### Checkout Code

This uses the `actions/checkout@v4.1.1` action to pull the repository code into the runner environment.

### AWS deployment actions

The subsequent steps (currently commented out) represent the actual deployment workflow to Amazon ECS. Here’s what each step does:

#### Configure AWS Credentials

Uses `aws-actions/configure-aws-credentials@v4.0.2` to set up AWS credentials, pulling them from GitHub secrets. This allows the workflow to interact with AWS resources securely. Note the user with `ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` was already described in the architecture proposal.

#### Download Task Definition

Retrieves the current ECS task definition and saves it as task-definition.json. This allows modifications to be made to the task before redeployment. Like new docker image path in the ECR.

#### Login to Amazon ECR

Logs into Amazon ECR (Elastic Container Registry) using `aws-actions/amazon-ecr-login@v2.0.1`, allowing the workflow to push the Docker image.

#### Create Entrypoint Script

- Sets up an entrypoint script to initialize the Django application:
  - Runs database migrations.
  - Starts the application using Gunicorn on port 8000.

#### Build, Tag, and Push Image to Amazon ECR

Builds the Docker image with the tag specified by the latest Git SHA, then pushes it to Amazon ECR.

#### Update ECS Task Definition

Replaces the container image in the ECS task definition with the newly built image using `aws-actions/amazon-ecs-render-task-definition@v1`.

#### Deploy to Amazon ECS

Deploys the updated ECS task definition to the `kaya` service on the `kayaCluster` ECS cluster. The `wait-for-service-stability` option ensures that the deployment completes successfully before moving on.

## Summary

This workflow is structured to:

- Ensure code quality checks are passed before deploying.
- Build a Docker image, push it to Amazon ECR, and deploy it to ECS.
- It’s modular, allowing for future uncommenting of deployment steps when deployment is required.
