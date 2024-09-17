"""Entrypoint for Vehicle-API"""

from aws_lambda_powertools.utilities.typing import (
  LambdaContext
)

from aws_lambda_powertools.event_handler import (
  APIGatewayRestResolver,
)

from aws_lambda_powertools import (
  Logger,
  Tracer,
)

from endpoints.v1 import (
  v1_router,
)

logger = Logger(log_uncaught_exceptions = True)
tracer = Tracer()

api = APIGatewayRestResolver(
# https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/#data-validation
  enable_validation = True,
# Add CORS for UI
)

api.enable_swagger(
  title   = "Vehicle-API",
  summary = "Vehicle-API {...}",
  version = "0.1.0-rc", # Todo: Extract from "pyproject.toml"
# {...}
)

# Prepare for API-Versions!

api.include_router(v1_router, prefix = "/v1")
# {..., prefix = "/v2"}
# {..., prefix = "/v3"}

@tracer.capture_lambda_handler()
def handler(request: dict, context: LambdaContext) -> dict:
  """Entrypoint for Vehicle-API"""
# context.identity => Can be used for various Python-Decorators like: @PreAuthorize("hasRole('Admin')")
  logger.append_keys(**context.__dict__)
  logger.debug("Request: '%s'", request)
  return api.resolve(
    request,
    context,
  )
