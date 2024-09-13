"""Entrypoint for Vehicle-API"""

from aws_lambda_powertools.event_handler import (
  APIGatewayRestResolver,
)

from aws_lambda_powertools import (
  Logger,
  Tracer,
)

from endpoints.v1 import (
  v1Router,
)

logger = Logger()
tracer = Tracer()

api = APIGatewayRestResolver(
# https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/#data-validation
  enable_validation = True,
# Add CORS for UI
)

api.enable_swagger(
  title   = "Vehicle-API",
  summary = "Vehicle-API {...}",
  version = "0.1.0-rc",
# {...}
)

# Prepare for API-Versions!

api.include_router(v1Router, prefix = "/v1")
# {..., prefix = "/v2"}
# {..., prefix = "/v3"}

@tracer.capture_lambda_handler()
def entrypoint(request: dict, context: dict) -> dict:
  """Entrypoint for REST-Api"""
  logger.debug("Received %s", request)
  return api.resolve(
    request,
    context,
  )
