from decorators import make_Table

from vehicle_api import dynamo, mapper
from vehicle_api import api_resolver

from fixtures import VehicleUpdateRequestFactory, VehicleFactory

import pytest
import json

entity1 = VehicleFactory.build()
entity2 = VehicleFactory.build()

TEST_CASES = [
  (200, VehicleUpdateRequestFactory.build(), entity1, entity1.id),
  (404, VehicleUpdateRequestFactory.build(), entity2, "404"),
]

dynamo = dynamo.Dynamo()
mapper = mapper.Mapper()

@make_Table
@pytest.mark.parametrize("status_code, update_request, entity, id", TEST_CASES)
def test_update(
  status_code:    int,
  update_request: any,
  entity:         any,
  id:             str) -> None:
  # Given
  dynamo.put(entity)
  # When
  event = {
    "httpMethod": "PUT",
    "path": f"/v1/{id}",
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
    item = dynamo.get(id)
    assert (
      mapper.as_DTO(item) ==
      body
    )
