"""Models for Vehicle-API"""

import inspect

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
    # {Only possible in Pydantic v1!}
    for field in fields:
      _class.__fields__[field].required = False
    return _class

  if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
    _class = fields[0]
    fields = _class.__fields__
    return func(_class)

  return func

def immutable(
  min_length: Optional[int] = None,
  max_length: Optional[int] = None,
  regex:      Optional[str] = None,
# {...}
) -> Field:
  """Immutable-Wrapper"""
  return Field(
    frozen = True, # => Makes any Attribute immutable after initial Assignment!
    min_length = min_length,
    max_length = max_length,
    regex = regex,
  )

class Shared(BaseModel):
  """
  Attributes shared across all Vehicle-Objects
  """
  Vin:       str = immutable(min_length = 17, max_length = 17)
  ModelType: str = immutable(max_length = 99)
  ModelName: str = immutable(max_length = 99)
  Power:     str = immutable(max_length = 3)
# {...}

class VehicleDTO(Shared):
  """
  Vehicle-DTO, exchanged with API-Users
  """
  Id:        str # = Immutable(regex = r"^{...}$")
  CreatedAt: str # = Immutable(regex = r"^{...}$")
  UpdatedAt: str # = Immutable(regex = r"^{...}$")

@optional_attrs
class VehicleUpdateRequest(Shared):
  """
  Model used To Update a Vehicle
  """

class VehicleCreateRequest(Shared):
  """
  Model used To Create a Vehicle
  """

class VehicleEntity(VehicleDTO):
  """
  Vehicle-Entity, saved in DB
  """
# ExpiresAt: int
  TracingId: str

# {...}
