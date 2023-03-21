from freezegun import freeze_time

from unittest.mock import patch

from vehicle_api import api_resolver
from vehicle_api import mapper

from fixtures import VehicleUpdateRequestFactory, VehicleFactory

import pytest
import json

TEST_CASES = [
  (200, VehicleUpdateRequestFactory.build(),                       VehicleFactory.build()),
  (404, VehicleUpdateRequestFactory.build(),                       None),
  (400, VehicleUpdateRequestFactory.build(True, vendor="Invalid"), None),
  (400, None,                                                      None),
]

mapper = mapper.Mapper()

@freeze_time("2025-01-01T00:00:00")
@pytest.mark.parametrize("status_code, update_request, entity", TEST_CASES)
def test_update(
  status_code:    int,
  update_request: any,
  entity:         any) -> None:
  # Given
  with (
    patch("vehicle_api.api_resolver.Dynamo.put"),
    patch("vehicle_api.api_resolver.Dynamo.get")
      as mock,
  ):
    mock.return_value = entity
    # When
    event = {
      "httpMethod": "PUT",
      "path": "/v1/id",
      "body": (
        json.dumps(update_request.dict()) if update_request != None
        else None
      )
    }
    resps = api_resolver.lambda_handler(event, {})
    # Then
    assert resps["statusCode"] == status_code

    if resps["statusCode"] == 200:
      body = json.loads(resps["body"])
      item = {
        **mapper.as_DTO(entity),
      # "createdAt": "2025-01-01T00:00:00",
        "updatedAt": "2025-01-01T00:00:00",
        **update_request.dict(),
      }
      assert item == body
