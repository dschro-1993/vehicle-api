"""V1-Endpoints"""

import env

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

Collection = env.COLLECTION

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
  d.delete_one(Collection, {"_id": id})
  # Idempotent Call => 200
  # {...}

@v1_router.get("/search")
def search(query: FilterCriteria) -> list[VehicleDTO]:
  """Todo"""
  # In Pydantic v2 please use:
  # {...}
  # class {...}
  #   @field_validator("sort", mode="before")
  #   def transform(cls, raw: dict) -> list[tuple[str, int]]:
  #     return [(k,v) for k,v in query.sort.items()]

  query.sort = [(k,v) for k,v in query.sort.items()]

  # Todo: Parse query => For unknown Attrs across: Filter, Aggregation, Sort, {...}

  r = d.search(Collection, **query.dict())
  return [
    mapper.as_DTO(
      VehicleEntity.parse_obj(x)
    ) for x in r
  ]

@v1_router.get("/<id>")
def search_one(id: str) -> VehicleDTO:
  """Todo"""
  result = d.search_one(Collection, {"_id": id})
  if result is None:
    raise ServiceError(404, f"No Vehicle was found in DB for: _id={id}")

  entity = VehicleEntity.parse_obj(result)
  return (
    mapper.as_DTO(
      entity
    )
  )

@v1_router.put("/<id>")
def update_one(id: str, body: VehicleUpdateRequest) -> VehicleDTO:
  """Todo"""
  update = {**body.dict(exclude_none=True), "UpdatedAt": datetime.now()}

  result = d.update_one(Collection, {"_id": id}, update)
  if result is None:
    raise ServiceError(404, f"No Vehicle was found in DB for: _id={id}")

  entity = VehicleEntity.parse_obj(result)
  return (
    mapper.as_DTO(
      entity
    )
  )

@v1_router.post("/")
def insert_one(body: VehicleCreateRequest) -> VehicleDTO:
  """Todo"""
  TracingId = v1_router.current_event["headers"]["X-Amzn-Trace-Id"]

  create = {**body.dict(exclude_none=True), "TracingId": TracingId}
  entity = VehicleEntity.parse_obj(create)

  d.insert_one(Collection, entity.dict(by_alias=True))
  return (
    mapper.as_DTO(
      entity
    )
  )

# {...}
