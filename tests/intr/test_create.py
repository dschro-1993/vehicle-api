from decorators import make_Table

from vehicle_api import dynamo, mapper
from vehicle_api import api_resolver

from fixtures import VehicleCreateRequestFactory

import json

dynamo = dynamo.Dynamo()
mapper = mapper.Mapper()

@make_Table
def test_create() -> None:
  # When
  event = {
    "httpMethod": "POST",
    "path": "/v1",
    "body": json.dumps(VehicleCreateRequestFactory.build().dict())
  }
  resps = api_resolver.lambda_handler(event, {})
  # Then
  assert resps["statusCode"] == 201

  body = json.loads(resps["body"])
  item = dynamo.get(body["id"])
  assert (
    mapper.as_DTO(item) ==
    body
  )
