from unittest.mock import patch, MagicMock

import api_resolver
import models

import pytest
import json
import os

def test_delete() -> None:
  # Idempotent Call => Always returns 204!
  # Given
  with (
    patch("vehicle_api.endpoints.v1.Dynamo.delete") as dynamoDeleteMock
  ):
    id = "a72edcc2-4a42-474e-becb-e11107f9524a"
    # When
    event = {"httpMethod": "DELETE", "path": f"/v1/{id}"}
    resps = api_resolver.entrypoint(event, {})
    # Then
    dynamoDeleteMock.assert_called_once_with(
      os.environ["TABLE_NAME"],
      {"Id": id},
    )
    assert (
      resps["statusCode"] ==
      200
    )
