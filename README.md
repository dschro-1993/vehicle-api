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
poetry run pytest tests/unit
```

### Intr

Prerequisite:
```
docker run -d -p 8000:8000 amazon/dynamodb-local
```

```
poetry run pytest tests/intr
```

## Deployment

Have a look at the Workflow.

## Smoke-Test

...

## Release

...
