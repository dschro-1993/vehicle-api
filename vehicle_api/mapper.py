"""Mapper for Vehicle-API"""

from typing import Union
from models import Vehicle

ToExclude = set() # Todo

class Mapper:
  """Mapper-Class"""
  def as_DTO(self, vehicle: Vehicle) -> Union[dict, None]:
    """
    Vehicle-Entity => DTO
    """
    return (
      vehicle.dict(exclude=ToExclude) if vehicle != None
      else None
    )
