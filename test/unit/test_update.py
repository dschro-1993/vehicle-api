import fixtures as f

from freezegun import freeze_time

from unittest.mock import patch, MagicMock

import api_resolver
import mapper
import models

import pytest
import json
import os

TEST_CASES = [
  (200, f.VehicleUpdateRequestFactory.build(),                      f.VehicleEntityFactory.build()),
  (404, f.VehicleUpdateRequestFactory.build(),                      None),
  (422, f.VehicleUpdateRequestFactory.build(True, Power="invalid"), None),
  (422, None,                                                       None),
]

mapper = mapper.Mapper()

@freeze_time("2025-01-01T00:00:00")
@pytest.mark.parametrize("status_code, update_request, entity", TEST_CASES)
def test_update(status_code: int, update_request: models.VehicleUpdateRequest, entity: models.VehicleEntity) -> None:
  # Given
  with (
    patch("vehicle_api.endpoints.v1.Dynamo.create") as dynamoCreateMock,
    patch("vehicle_api.endpoints.v1.Dynamo.lookup") as dynamoLookupMock,
  ):
    dynamoLookupMock.return_value = entity.dict() if entity != None else None
    # When
    event = {
      "httpMethod": "PUT",
      "headers": {"X-Amzn-Trace-Id": "foo"},
      "path": "/v1/a72edcc2-4a42-474e-becb-e11107f9524a",
      "body": (
        json.dumps(update_request.dict()) if update_request != None else None
      )
    }
    resps = api_resolver.entrypoint(event, {})
    # Then
    assert resps["statusCode"] == status_code

    if resps["statusCode"] == 200:
      item = {
        **mapper.as_DTO(entity).dict(),
      # "CreatedAt": "2025-01-01T00:00:00",
        "UpdatedAt": "2025-01-01T00:00:00",
        **update_request.dict(),
      }
      entity = models.VehicleEntity(**{"TracingId": entity.TracingId, **item})
      dynamoCreateMock.assert_called_once_with(
        os.environ["TABLE_NAME"],
        entity.dict(),
      )
      body = json.loads(resps["body"])
      assert item == body

    # {...}
