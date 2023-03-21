from freezegun import freeze_time

from unittest.mock import patch

from vehicle_api import api_resolver

from fixtures import VehicleCreateRequestFactory

import pytest
import json

TEST_CASES = [
  (201, VehicleCreateRequestFactory.build()),
  (400, VehicleCreateRequestFactory.build(True, vendor="Invalid")),
  (400, None),
]

@freeze_time("2025-01-01T00:00:00")
@pytest.mark.parametrize("status_code, create_request", TEST_CASES)
def test_create(
  status_code:    int,
  create_request: any) -> None:
  # Given
  with (
    patch("vehicle_api.api_resolver.Dynamo.put") as mock,
    patch("vehicle_api.api_resolver.uuid4")      as uuid,
  ):
    id = "id"
    uuid.return_value = id
    # When
    event = {
      "httpMethod": "POST",
      "path": "/v1",
      "body": (
        json.dumps(create_request.dict()) if create_request != None
        else None
      )
    }
    resps = api_resolver.lambda_handler(event, {})
    # Then
    assert resps["statusCode"] == status_code

    if resps["statusCode"] == 201:
      body = json.loads(resps["body"])
      item = {
        **create_request.dict(),
        "createdAt": "2025-01-01T00:00:00",
        "updatedAt": "2025-01-01T00:00:00",
        "id": id,
      }
      assert item == body
