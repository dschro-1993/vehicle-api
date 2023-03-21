from unittest.mock import patch

from vehicle_api import api_resolver

def test_delete() -> None:
  # Idempotency => Delete always returns 204
  with (
    patch("vehicle_api.api_resolver.Dynamo.delete")
      as mock
  ):
    # When
    event = {"httpMethod": "DELETE", "path": "/v1/id"}
    resps = api_resolver.lambda_handler(event, {})
    # Then
    assert (
      resps["statusCode"] ==
      204
    )
