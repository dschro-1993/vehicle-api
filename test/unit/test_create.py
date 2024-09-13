import fixtures as f

from freezegun import freeze_time

from unittest.mock import patch, MagicMock

import api_resolver
import models

import pytest
import json
import os

TEST_CASES = [
  (200, f.VehicleCreateRequestFactory.build()),
  (422, f.VehicleCreateRequestFactory.build(True, Power="invalid")),
  (422, None),
]

@freeze_time("2025-01-01T00:00:00")
@pytest.mark.parametrize("status_code, create_request", TEST_CASES)
def test_create(status_code: int, create_request: models.VehicleCreateRequest) -> None:
  # Given
  with (
    patch("vehicle_api.endpoints.v1.Dynamo.create") as dynamoCreateMock,
    patch("vehicle_api.endpoints.v1.uuid.uuid4")    as uuidv4Mock,
  ):
    id = "a72edcc2-4a42-474e-becb-e11107f9524a"
    uuidv4Mock.return_value = id
    TracingId = "1234"
    # When
    event = {
      "httpMethod": "POST",
      "headers": {"X-Amzn-Trace-Id": TracingId},
      "path": "/v1",
      "body": (
        json.dumps(create_request.dict()) if create_request != None else None
      )
    }
    resps = api_resolver.entrypoint(event, {})
    # Then
    assert resps["statusCode"] == status_code

    if resps["statusCode"] == 200:
      item = {
        **create_request.dict(),
        "CreatedAt": "2025-01-01T00:00:00",
        "UpdatedAt": "2025-01-01T00:00:00",
        "Id": id,
      }
      entity = models.VehicleEntity(**{"TracingId": TracingId, **item})
      dynamoCreateMock.assert_called_once_with(
        os.environ["TABLE_NAME"],
        entity.dict(),
      )
      body = json.loads(resps["body"])
      assert item == body

    # {...}
