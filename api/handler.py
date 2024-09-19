"""Entrypoint for Vehicle-API"""

from aws_lambda_powertools.utilities.typing import (
  LambdaContext
)

from aws_lambda_powertools.event_handler.middlewares import NextMiddleware

from aws_lambda_powertools.event_handler import (
  APIGatewayRestResolver,
  Response,
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

def _is_valid(Token: str | None) -> bool:
  return False

def swagger_middleware(api: APIGatewayRestResolver, middleware: NextMiddleware) -> Response:
  Token = api.current_event.headers["Authorization"]
# {...}
  if _is_valid(Token):
    return middleware(api)

  return (
    Response(
      400
    )
  )

api.enable_swagger(
  title   = "Vehicle-API",
  summary = "Vehicle-API {...}",
  version = "0.1.0", # Todo: Extract from "pyproject.toml"
  middlewares = [swagger_middleware],
# {...}
)

# Prepare for API-Versions!

api.include_router(v1_router, prefix = "/v1")
# {..., prefix = "/v2"}
# {..., prefix = "/v3"}

@tracer.capture_lambda_handler()
def _handler(request: dict, context: LambdaContext) -> dict:
  """Entrypoint for Vehicle-API"""
# context.identity => Can be used for various Python-Decorators like: @PreAuthorize("hasRole('Admin')")
  logger.append_keys(**context.__dict__)
  logger.debug("Request: '%s'", request)
  return api.resolve(
    request,
    context,
  )
