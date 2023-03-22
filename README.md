# Vehicle-API

## Overview

<!-- ![.](./docs/overview.jpg) -->
<img src="./docs/overview.jpg" width="750" height="650">

## Prerequisites

- Terraform
- Python3.9
- Poetry

## Installation

```
poetry install
```

## Pylint

```
pylint vehicle_api/
```

## Pytest

### Unit

```
coverage run -m pytest tests/unit
coverage report -m
```

### Intr

Prerequisite:
```
docker run -d -p 8000:8000 amazon/dynamodb-local
```

```
coverage run -m pytest tests/intr
coverage report -m
```

## Deployment

...

## Smoke-Test

...

## Release

...
