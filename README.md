# Vehicle-API

## Introduction

This Repository just serves as a HTTP-/REST-driven Serverless-Blueprint on AWS.

(AppSync-Wrapper for GraphQL-Support is planned/WIP)

## Architecture

<!-- ![.](./docs/overview.jpg) -->
<img src="./docs/overview.jpg" width="750" height="650">

## Prerequisites

- Terraform (Recommendation: tfenv)
- Python3.9 (Recommendation: pyenv)
- Poetry

## OpenAPI Spec

An always up-to-date Version of this API can be found [here](./openapi.yml).

This is your Source of Truth of this API as it is also used within Terraform where we define/deploy our API-Gateway.
It defines all our:
- Endpoints (Create, Update, Delete, Find-By-ID, ...)
  - With a Version-Prefix: v1 (for now)
- In- and Outputs

## Infra

### Terraform

All required AWS Resources of this API were defined in a separate [Terraform Module](https://github.com/dschro-1993/vehicle-api-terraform-module).

(Git Tagging is used)

Just to be able to reuse them for Deployments on:
```
- feature branch -> ./terraform/qa
- main    branch -> ./terraform/prod
```

### API Gateway

The API Gateway itself is defined/deployed based on our OpenAPI-Spec.

#### R53

A Custom Domain (in a Public-Hosted Zone) was created to be able to fetch/query Vehicles on a fixed/static Domain.

Additional Domain-Mappinq was created on our API-Gateway to make this API available via:
```
- qa   -> vehicle-api-qa  .292372118261.starfish-rentals.com/v1
- prod -> vehicle-api-prod.292372118261.starfish-rentals.com/v1
```

#### ACM

A custom TLS-Certificate for this API / Custom Domain was created via ACM.
(DNS-based Validation)

#### WAF

A WAF (Web Application Firewall) was created which contains:
- Few AWS Manaqed Rule-Sets (specifically recommended for Web-Applications)
- [RateBased-Rules/-Blocker](https://aws.amazon.com/blogs/security/three-most-important-aws-waf-rate-based-rules/)

### DynamoDB

For Billinq-Mode "Pay-Per-Request" was enabled to scale On-Demand. (As any exact Traffic-Patterns are unknown yet).

On prod, PITR (Point-In-Time Recovery) was enabled to rollback data in case it will be corrupted - by test-scripts.

### lambda

The API is 100% serverless-based and served by the λ-Service, and so is very cost-effective.

## Application Overview

The Application heavily uses [AWS lambda PowerTools for Python](https://awslabs.github.io/aws-lambda-powertools-python/2.10.0/) (Introduced @[AWS re:Invent 2022](https://portal.awsevents.com/events/reInvent2022/sessions/opn306)).

This way we avoid lots of DRY-Code and have access to lots of additional/helpful Utilities such as:
- custom-metrics
- tracer
- loqqer
- ...

The Application is structured as follows:
```
./vehicle_api:
  - api-resolver.py # Main Router/Controller for all HTTP-/REST-Endpoints
  - mapper.py       # Mapper between Entities/DTOs and vice versa
  - models.py       # Models -> all Input-/Output-Objects for API
  - dynamo.py       # Repository/Persistence-layer
```

Every Endpoint is served by one main λ-Function. This has a few **benefits**:

- Complexity of API is very low (Compared to: Bundle/Deploy and Maintain one Function per Endpoint)
- Chance     of a cold start is heavily reduced

### Dependencies

The Application uses the followinq Dependencies @Runtime:

```
- aws-lambda-powertools (Contains Pydantic for Validation already)
- boto3
```

#### λ-Layers

We can skip to bundle these Dependencies ourselves. There are already official λ-Layers.\
*(boto3 excluded - already available in λ-Service)*

```
- arn:aws:lambda:<REGION>:017000801446:layer:AWSLambdaPowertoolsPythonV2-Arm64:<VERSION>
```

## Installation

```
poetry install
```

## Pylint

```
On Poetry -> pylint vehicle_api/
```

## Pytest

### Unit

```
On Poetry -> poetry run pytest tests/unit
```

### Intr

Prerequisite:
```
docker run -d -p 8000:8000 amazon/dynamodb-local
```

```
On Poetry -> poetry run pytest tests/intr
```

## Deployment

Have a look at the Workflow.

## Smoke-Test

...

## CICD-Pipeline

...

## Release

...
