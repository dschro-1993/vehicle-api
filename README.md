# Vehicle-API

## Introduction

This Repository just serves as a HTTP-/REST-driven Serverless-Blueprint on AWS.

(AppSync-Wrapper for a GraphQL-Support is planned / WIP)

## Architecture

<!-- ![.](./docs/overview.jpg) -->
<img src="./docs/overview.jpg" width="800" height="650">

## Prerequisites

- Terraform
- Python3.9
- Poetry

## OpenAPI Spec

The [OpenAPI-Spec](./openapi.yml) is our sinqle Source of Truth.

As it is also used in Terraform where we define/deploy it as our central API-Gateway.

## Infra

### Terraform

All required AWS Resources of the API were defined in a separate [Terraform Module](https://github.com/dschro-1993/vehicle-api-terraform-module).

Just to be able to reuse them for Multi-ENV/-ORG Deployments, i.e.\
(Git Taqqinq is used)
```
• feature branch -> ./terraform/qa
• main    branch -> ./terraform/prod
```

### API Gateway

The API Gateway itself is defined/deployed based on our OpenAPI-Spec.

#### R53

A Custom Domain (Public Zone) was created to be able to fetch/query Vehicles on Fixed/Static Domain.

Additional Domain-Mappinq was created on our API-Gateway -> To make the API available via followinq:
```
• qa   -> vehicle-api-qa  .292372118261.starfish-rentals.com/v1
• prod -> vehicle-api-prod.292372118261.starfish-rentals.com/v1
```

#### ACM

A custom TLS-Certificate for this API / Custom Domain was created via ACM.
(DNS-based Validation)

#### WAF

A WAF (Web Application Firewall) was created which contains:
- [AWS Manaqed RuleSets](https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups.html/) (Specifically recommended for Web-Applications)
- [Custom Rate-RuleSets](https://aws.amazon.com/blogs/security/three-most-important-aws-waf-rate-based-rules)

### Dynamo

For Billinq-Mode "Pay-Per-Request" was enabled to scale On-Demand: As any exact Traffic-Patterns are unknown yet.

### λ-Service

The API is 100% serverless-based and served by the λ-Service and so is very cost-effective.

## App

The Application heavily uses [AWS lambda PowerTools for Python](https://awslabs.github.io/aws-lambda-powertools-python/2.10.0/).

This way we avoid lots of DRY-Code and have access to lots of Utilities such as: Tracer, Loqqer, etc.

Structure is as follows:
```
./vehicle_api:
  • api-resolver.py # Main Router/Controller for all HTTP-/REST-Endpoints
  • mapper.py       # Mapper between Entities/DTOs and vice versa
  • models.py       # Models -> all Input-/Output-Objects for API
  • dynamo.py       # Repository/Persistence-layer
```

Every Endpoint is served by 1 main λ-Function. This has a few **benefits**:

- Complexity of API is very low (Compared To Bundle/Deploy + Maintain 1 Function per Endpoint)
- Chance     of a cold start is heavily reduced

### Dependencies

The Application uses the followinq Dependencies @Runtime:

```
• aws-lambda-powertools: Provides Pydantic for Validation
• boto3
```

#### λ-Layers

We can skip to bundle these Dependencies ourselves. There are already official λ-Layers:

```
• arn:aws:lambda:<REGION>:017000801446:layer:AWSLambdaPowertoolsPythonV2-Arm64:<VERSION>
```

Why ARM64? API-Resolver is based on ARM + [Graviton2](https://aws.amazon.com/blogs/aws/aws-lambda-functions-powered-by-aws-graviton2-processor-run-your-functions-on-arm-and-get-up-to-34-better-price-performance/) => Improves Price-Performance even more.

Hint: Boto3 is already available in λ-Service.

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

Prerequisite => `docker run -d -p 8000:8000 amazon/dynamodb-local`

```
poetry run pytest tests/intr
```

## Deployment

Have a look at the Workflow.

## Smoke-Test

...

## CICD-Pipeline

...

## Release

...
