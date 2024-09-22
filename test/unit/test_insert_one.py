import fixtures as f

from freezegun import freeze_time

from unittest.mock import patch, MagicMock

import handler
import models

import pytest
import json
import os

TEST_CASES = [
  (200, f.VehicleCreateRequestFactory.build()),
  (422, f.VehicleCreateRequestFactory.build(True, Vin="invalid")),
  (422, None),
]

@freeze_time("2025-01-01T00:00:00")
@pytest.mark.parametrize("status_code, create_request", TEST_CASES)
def test_create(
  status_code:    int,
  create_request: models.VehicleCreateRequest,
) -> None:
  pass
# {..}
