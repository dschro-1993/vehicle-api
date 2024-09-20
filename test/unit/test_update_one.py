import fixtures as f

from freezegun import freeze_time

from unittest.mock import patch, MagicMock

import api_resolver
import mapper
import models

import pytest
import json
import os

TEST_CASES = [
  (200, f.VehicleUpdateRequestFactory.build(),                    f.VehicleEntityFactory.build()),
  (404, f.VehicleUpdateRequestFactory.build(),                    None),
  (422, f.VehicleUpdateRequestFactory.build(True, Vin="invalid"), None),
  (422, None,                                                     None),
]

mapper = mapper.Mapper()

@freeze_time("2025-01-01T00:00:00")
@pytest.mark.parametrize("status_code, update_request, entity", TEST_CASES)
def test_update(
  status_code:    int,
  update_request: models.VehicleUpdateRequest,
  entity:         models.VehicleEntity,
) -> None:
  pass
# {..}
