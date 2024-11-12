# Application Deployment to AWS

## Services

- VPC
- Amazon Elastic Container Registry
- Amazon Elastic Container Services
- Security groups
- Application Load Balancer
- Amazon EC2 Auto Scaling
- Amazon EC2
- AWS Simple Cloud Storage
- Amazon Cloud Watch
- Amazon RDS for PostgreSQ
- Amazon Route 53
- AWS Certificate Manager
- IAM users

## Proposed Architecture

### VPC and Subnets

Start by creating a new Virtual Private Cloud (VPC) in the region where the API will primarily be used. Set up at least two subnets within this VPC:

- A private subnet for resources not exposed to internet traffic (such as the PostgreSQL database).
- A public subnet for the Application Load Balancer and other public-facing resources.

### Security Groups

Define at least two security groups to control access to resources:

- A security group that restricts database access to selected EC2 instances only.
- A security group that allows only the Application Load Balancer to access the EC2 instances.

### Database and Monitoring

Deploy an Amazon RDS instance for PostgreSQL within the private subnet. Set up Amazon CloudWatch for production-level logging and enable auto-scaling to handle variable loads.

### Static Content Storage

Create an S3 bucket for storing static assets of the Django application.

### Domain and SSL

For custom domain needs, consider purchasing a domain from Route 53 or an external provider like GoDaddy.
Obtain a free SSL certificate from AWS Certificate Manager to enable HTTPS for the custom domain.

### Container Registry and Task Definition

- Create a new Amazon Elastic Container Registry (ECR) to store your Docker images. Note the ARN of the ECR repository.
- Define an ECS task with the necessary environment variables, CloudWatch configurations, and resource requirements (CPU and memory).
Include the correct ECR ARN in the task definition.

### Cluster and Service Setup

Create an ECS cluster and deploy a service within it.
Ensure the service uses the appropriate version of the task definition.

### IAM User for CI/CD

Create a new IAM user specifically for CI/CD purposes. Generate access keys for this user but do not grant console access.
Attach a custom policy that permits access to only the ECR repository, ECS cluster, and ECS service.
