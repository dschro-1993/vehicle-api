"""V1-Endpoints"""

from env_vars import COLLECTION_NAME

from datetime import datetime

from aws_lambda_powertools.event_handler.exceptions import (
  ServiceError
)

from aws_lambda_powertools import (
  event_handler,
  Logger,
)

from mapper import Mapper

from models import (
  FilterCriteria,
  VehicleCreateRequest,
  VehicleUpdateRequest,
  VehicleEntity,
  VehicleDTO,
)

from db import DB

import os

v1_router = event_handler.api_gateway.Router()

mapper = Mapper()
logger = Logger()

d = DB()

# --- Experimental Stuff

# To Show i.e.:
# - How To Add and Use any Custom-Requirement => like "requests"?
# - {...} 

# @v1_router.get("/foobaz")
# def foobaz(q: typing.Annotated[str, Query(pattern=r"^\d{12}$")]) -> dict:
#   r = requests.get(f"https://www.google.com?q={q}", timeout=10)
#   logger.info(r)
#   return r

# --- Vehicle

@v1_router.delete("/<id>")
def delete_one(id: str) -> None:
  """Todo"""
  d.delete_one(COLLECTION_NAME, {"_id": id})
  # Idempotent Call => 200
  # {...}

@v1_router.get("/search")
def search(criteria: FilterCriteria) -> list[VehicleDTO]:
  """Todo"""
# {...}
  criteria.sort = [(key, val) for key, val in criteria.sort.items()]

# if criteria.limit and criteria.limit > LIMIT_MAXIMUM: # => Could also be handled via Pre-Validator in Pydantic v2!
#    criteria.limit = LIMIT_MAXIMUM

  r = d.search(COLLECTION_NAME, **criteria.dict())
  return [
    mapper.as_DTO(
      VehicleEntity.parse_obj(x), # {}
    ) for x in r
  ]

@v1_router.get("/<id>")
def search_one(id: str) -> VehicleDTO:
  """Todo"""
  result = d.search_one(COLLECTION_NAME, {"_id": id})
  if result is None:
    raise ServiceError(404, f"No Vehicle has been found for '_id={id}'")

  entity = VehicleEntity.parse_obj(result)
  return (
    mapper.as_DTO(
      entity,
    # {}
    )
  )

@v1_router.put("/<id>")
def update_one(id: str, r_body: VehicleUpdateRequest) -> VehicleDTO:
  """Todo"""
  update = {
    **r_body.dict(exclude_none=True), # model_dump() in Pydantic v2!
  # "CreatedAt": datetime.now(),
    "UpdatedAt": datetime.now(),
  }

  # Atomic Operation
  result = d.search_one_and_update(COLLECTION_NAME, {"_id": id}, update)
  if result is None:
    raise ServiceError(404, f"No Vehicle has been found for '_id={id}'")

  entity = VehicleEntity.parse_obj(result)
  return (
    mapper.as_DTO(
      entity,
    # {}
    )
  )

@v1_router.post("/")
def insert_one(r_body: VehicleCreateRequest) -> VehicleDTO:
  """Todo"""
  logger.info(os.environ["_X_AMZN_TRACE_ID"])
  insert = {
    **r_body.dict(),
    "TracingId": v1_router.current_event["headers"]["X-Amzn-Trace-Id"],
  # {...}
  }
  entity = VehicleEntity.parse_obj(insert)

  d.insert_one(COLLECTION_NAME, entity.dict(by_alias=True))
  return (
    mapper.as_DTO(
      entity,
    # {}
    )
  )

# {...}
