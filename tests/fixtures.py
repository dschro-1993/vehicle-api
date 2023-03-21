from pydantic_factories import ModelFactory

from vehicle_api import models

class VehicleCreateRequestFactory(ModelFactory):
  __model__ = models.VehicleCreateRequest

class VehicleUpdateRequestFactory(ModelFactory):
  __model__ = models.VehicleUpdateRequest

class VehicleFactory(ModelFactory):
  __model__ = models.Vehicle
