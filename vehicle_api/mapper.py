"""Mapper for Vehicle-API"""

from models import (
  VehicleEntity,
  VehicleDTO,
)

class Mapper:
  """Mapper-Class for DDD => https://martinfowler.com/bliki/DomainDrivenDesign.html"""
  def as_DTO(self, entity: VehicleEntity) -> VehicleDTO:
    """
    Transforms VehicleEntity => VehicleDTO
    """
    return VehicleDTO(
      **entity.dict( # => model.model_dump({...}) in v2!
        exclude = {
          "TracingId",
        # {...}
        }
      )
    )
