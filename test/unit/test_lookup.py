import fixtures as f

from unittest.mock import patch, MagicMock

import api_resolver
import mapper
import models

import pytest
import json
import os

TEST_CASES = [
  (200, f.VehicleEntityFactory.build()),
  (404, None),
]

mapper = mapper.Mapper()

@pytest.mark.parametrize("status_code, entity", TEST_CASES)
def test_lookup(status_code: int, entity: models.VehicleEntity) -> None:
  # Given
  with (
    patch("vehicle_api.endpoints.v1.Dynamo.lookup") as dynamoLookupMock
  ):
    id = "a72edcc2-4a42-474e-becb-e11107f9524a"
    dynamoLookupMock.return_value = entity.dict() if entity != None else None
    # When
    event = {"httpMethod": "GET", "path": f"/v1/{id}"}
    resps = api_resolver.entrypoint(event, {})
    # Then
    dynamoLookupMock.assert_called_once_with(
      os.environ["TABLE_NAME"],
      {"Id": id},
    )
    assert resps["statusCode"] == status_code

    if resps["statusCode"] == 200:
      body = json.loads(resps["body"])
      assert (
        mapper.as_DTO(entity) ==
        body
      )
