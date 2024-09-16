"""Models for Vehicle-API"""

import inspect

from datetime import datetime

from uuid import (
  uuid4,
  UUID,
)

from typing import (
  Callable,
  Optional,
)

from pydantic import (
  BaseModel,
  Field,
)

def optional_attrs(*fields) -> Callable:
  """
  Taken from: https://github.com/samuelcolvin/pydantic/issues/1223#issuecomment-775363074
  """
  def func(_class):
    # It loops over Class-Fields and sets Pydantic-Attribute "required" = False
    # {Works only in Pydantic v1!}
    for field in fields:
      _class.__fields__[field].required = False
    return _class

  if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
    _class = fields[0]
    fields = _class.__fields__
    return func(_class)

  return func

class FilterCriteria(BaseModel):
  filter:      dict = {}
  aggregation: dict = {}
  sort:        dict = {}
  limit:       int  = 50 # => Todo: Env-Var + MAX_VALUE ...
  skip:        int  = 0

class Shared(BaseModel):
  """
  Attributes shared across all Vehicle-Objects
  """
  Vin:       str = Field(frozen = True, min_length = 17, max_length = 17)
  ModelType: str = Field(frozen = True, max_length = 99)
  ModelName: str = Field(frozen = True, max_length = 99)
  Power:     int = Field(frozen = True, lt = 1500)
# {...}

@optional_attrs
class VehicleUpdateRequest(Shared):
  """
  Model used To Update a Vehicle
  """

class VehicleCreateRequest(Shared):
  """
  Model used To Create a Vehicle
  """

def _uuid4_as_str() -> str:
  return str(uuid4())

class VehicleEntity(Shared):
  """
  Vehicle-Entity, saved in DB
  """
  CreatedAt: datetime = Field(default_factory = datetime.now)
  UpdatedAt: datetime = Field(default_factory = datetime.now)
  TracingId: str
  Id:        str = Field(default_factory = _uuid4_as_str, alias = "_id")

class VehicleDTO(Shared):
  """
  Vehicle-DTO
  """
  CreatedAt: datetime
  UpdatedAt: datetime
  Id:        str

# {...}
