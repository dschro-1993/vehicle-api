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
def search(query: FilterCriteria) -> list[VehicleDTO]:
  """Todo"""
# {...}
  query.sort = [(key, val) for key, val in query.sort.items()]

# if query.limit and query.limit > LIMIT_MAXIMUM:
#    query.limit = LIMIT_MAXIMUM

  # Todo: Parse query => For unknown Attrs across: Filter, Aggregation, Sort, {...}

  r = d.search(COLLECTION_NAME, **query.dict())
  return [
    mapper.as_DTO(
      VehicleEntity.parse_obj(x)
    ) for x in r
  ]

@v1_router.get("/<id>")
def search_one(id: str) -> VehicleDTO:
  """Todo"""
  result = d.search_one(COLLECTION_NAME, {"_id": id})
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

  result = d.update_one(COLLECTION_NAME, {"_id": id}, update)
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
# TracingId = v1_router.current_event["headers"]["X-Amzn-Trace-Id"]

  create = {**body.dict(exclude_none=True), "TracingId": "1234567"}
  entity = VehicleEntity.parse_obj(create)

  d.insert_one(COLLECTION_NAME, entity.dict(by_alias=True))
  return (
    mapper.as_DTO(
      entity
    )
  )

# {...}
