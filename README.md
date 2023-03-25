# Vehicle-API

## Introduction

This Repository serves as a Serverless-Blueprint on AWS. Supports: REST + GraphQL (AppSync)

## Architecture

<!-- ![.](./docs/overview.jpg) -->
<img src="./docs/overview.jpg" width="600" height="700">

## Prerequisites

- Terraform
- Python3.9
- Poetry

## GraphQL

...

## OpenAPI

...

## Infra

### Terraform

All required AWS Resources were defined in a separate [Terraform Module](https://github.com/dschro-1993/vehicle-api-terraform-module).

To be reused for:
```
• feature branch -> ./terraform/qa
• main    branch -> ./terraform/prod
```

### API Gateway

The API Gateway itself is defined/deployed based on our OpenAPI-Spec.

#### R53

Todo => GraphQL
```
• qa   -> vehicle-api-qa  .292372118261.starfish-rentals.com/v1
• prod -> vehicle-api-prod.292372118261.starfish-rentals.com/v1
```

#### ACM

TLS-Certificate for this API was created via ACM. (DNS-based Validation)

#### WAF

A WAF (Web Application Firewall) was created which contains:
- AWS Manaqed RuleSets
- Custom Rate-RuleSets

### DocumenT-DB

...

### λ-Service

The API is 100% serverless-based / served by λ-Service and so is very cost-effective.

## App

The Application heavily uses [AWS lambda PowerTools for Python](https://awslabs.github.io/aws-lambda-powertools-python/2.10.0/).

This way we avoid lots of DRY-Code + have access to lots of Utilities such as: Tracer, Loqqer, etc.

Structure is as follows:
```
./vehicle_api:
  • api-resolver.py # Main Controller for all HTTP-/REST- and GraphQL-Endpoints
  • mapper.py       # Mapper between Entities/DTOs and vice versa
  • models.py       # Models -> all Input-/Output-Objects for API
  • dynamo.py       # Repository/Persistence-layer
```

Every Endpoint is served by one main λ-Function. This has various **benefits**:

- Complexity of API is very low (Compared To => Bundle/Deploy + Maintain one Function per Endpoint)
- Chance     of a cold start is heavily reduced

### Dependencies

The Application uses The followinq Dependencies @Runtime:

```
• aws-lambda-powertools => Pydantic
• requests
• py-mongo
```

#### λ-Layers

```
• arn:aws:lambda:<REGION>:017000801446:layer:AWSLambdaPowertoolsPythonV2-Arm64:<VERSION>
```

Why ARM64? The API-Resolver is based on Graviton2. Improves Price-Performance even more.

## Installation

```
poetry install
```

## Pytest

### Unit

```
poetry run pytest tests/unit
```

### Intr

Prerequisite => `docker run -d -p 27017:27017 mongo:4`

```
poetry run pytest tests/intr
```

## Deployment

Have a look at The Workflow.

## Smoke-Test

...

## CICD-Pipeline

...

## Release

...
