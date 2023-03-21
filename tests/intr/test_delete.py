from decorators import make_Table

from vehicle_api import dynamo
from vehicle_api import api_resolver

from fixtures import VehicleFactory

dynamo = dynamo.Dynamo()

@make_Table
def test_delete() -> None:
  # Given
  entity = VehicleFactory.build()
  dynamo.put(entity)
  # 1st: Assert if Vehicle was created in DynamoDB Table
  result = dynamo.get(entity.id)
  assert result != None
  # When
  event = {"httpMethod": "DELETE", "path": f"/v1/{entity.id}"}
  resps = api_resolver.lambda_handler(event, {})
  # Then
  assert resps["statusCode"] == 204
  # 2nd: Assert if Vehicle was deleted in DynamoDB Table
  result = dynamo.get(entity.id)
  assert result is None
