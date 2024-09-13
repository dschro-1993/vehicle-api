"""V1-Endpoints"""

import os
import uuid
import typing

from datetime import datetime

import boto3
import requests

from aws_lambda_powertools.event_handler.openapi.params import Query

from aws_lambda_powertools.event_handler.exceptions import (
  ServiceError
)

from aws_lambda_powertools import (
  event_handler,
  Logger,
)

from cross_account import assume_role_for_account_id

from dynamo import Dynamo
from mapper import Mapper

from models import (
  VehicleCreateRequest,
  VehicleUpdateRequest,
  VehicleEntity,
  VehicleDTO,
)

VehicleTableName = os.environ["TABLE_NAME"]

v1Router = event_handler.api_gateway.Router()

dynamo = Dynamo()
mapper = Mapper()
logger = Logger()

# --- Experimental Stuff

# To Show i.e.:
# - How To Include and Use Custom-Requirements, i.e. like "requests"
# - How To Make Cross-Account Calls and How To Cache STS-Credentials
# - {...} 

@v1Router.get("/Volumes")
def search(account_id: typing.Annotated[str, Query(pattern=r"^\d{12}$")]) -> dict:
  """..."""
  req = requests.get("HTTPS://www.google.com", timeout=10)
  logger.debug(req)

  assume = assume_role_for_account_id(account_id)
  if assume is None:
    raise ServiceError(404, f"No Account was found for 'account_id={account_id}'")

  client = boto3.client("ec2", aws_access_key_id=assume["AccessKeyId"], aws_secret_access_key=assume["SecretAccessKey"], aws_session_token=assume["SessionToken"])
  return (
    client
    .describe_volumes(
    # VolumeIds=[]
    # Filters=[]
    # {...}
    )
  )

# --- Vehicle Crud-Ops

@v1Router.delete("/<id>")
def delete(id: str) -> None:
  """Delete Vehicle"""
  dynamo.delete(VehicleTableName, {"Id": id})
  # Idempotent Call => 200

def lookup_by_id(id: str) -> dict:
  item = dynamo.lookup(VehicleTableName, {"Id": id})
  if item is None:
    raise ServiceError(404, f"No Vehicle Found was found for id={id}")
  return item

@v1Router.get("/<id>")
def lookup(id: str) -> VehicleDTO:
  """Lookup Vehicle"""
  item = lookup_by_id(id)

  return (
    mapper.as_DTO(
      VehicleEntity(
        **item
      )
    )
  )

@v1Router.put("/<id>")
def update(body: VehicleUpdateRequest, id: str) -> VehicleDTO:
  """Update Vehicle"""
  item = lookup_by_id(id)

  timestamp = datetime.now().isoformat()
  entity = VehicleEntity(**{ # Improve => How To combine Body + internal Values w/o wrapping into a new Object?
    **item,
    # As 2nd, To Override Attrs from found Item!
    **body.dict(exclude_none = True),
  # "CreatedAt": timestamp,
    "UpdatedAt": timestamp,
  })
  dynamo.create(VehicleTableName, entity.dict())
  return (
    mapper.as_DTO(
      entity
    )
  )

@v1Router.post("/")
def create(body: VehicleCreateRequest) -> VehicleDTO:
  """Create Vehicle"""
  timestamp = datetime.now().isoformat()
  entity = VehicleEntity(**{ # Improve => How To combine Body + internal Values w/o wrapping into a new Object?
    **body.dict(exclude_none = True),
    "TracingId": v1Router.current_event["headers"]["X-Amzn-Trace-Id"],
    "CreatedAt": timestamp,
    "UpdatedAt": timestamp,
    "Id": str(uuid.uuid4()),
  })
  dynamo.create(VehicleTableName, entity.dict())
  return (
    mapper.as_DTO(
      entity
    )
  )
