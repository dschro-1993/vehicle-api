from pydantic_factories import ModelFactory

from models import (
  VehicleCreateRequest,
  VehicleUpdateRequest,
  VehicleEntity,
# {...}
)

class MyModelFactory(ModelFactory):
  __allow_none_optionals__ = False

class VehicleCreateRequestFactory(MyModelFactory):
  __model__ = VehicleCreateRequest

class VehicleUpdateRequestFactory(MyModelFactory):
  __model__ = VehicleUpdateRequest

class VehicleEntityFactory(MyModelFactory):
  __model__ = VehicleEntity

# {...}
