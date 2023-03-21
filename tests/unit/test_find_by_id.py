from unittest.mock import patch

from vehicle_api import api_resolver
from vehicle_api import mapper

from fixtures import VehicleFactory

import pytest
import json

TEST_CASES = [
  (200, VehicleFactory.build()),
  (404, None),
]

mapper = mapper.Mapper()

@pytest.mark.parametrize("status_code, entity", TEST_CASES)
def test_find_by_id(
  status_code: int,
  entity:      any) -> None:
  # Given
  with (
    patch("vehicle_api.api_resolver.Dynamo.get")
      as mock
  ):
    mock.return_value = entity
    # When
    event = {"httpMethod": "GET", "path": "/v1/id"}
    resps = api_resolver.lambda_handler(event, {})
    # Then
    assert resps["statusCode"] == status_code

    if resps["statusCode"] == 200:
      body = json.loads(resps["body"])
      assert (
        mapper.as_DTO(entity) ==
        body
      )
