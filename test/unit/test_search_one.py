import fixtures as f

from unittest.mock import patch, MagicMock

import handler
import mapper
import models

import pytest
import json
import os

TEST_CASES = [
  (200, f.VehicleEntityFactory.build()),
  (404, None),
]

mapper = mapper.Mapper()

@pytest.mark.parametrize("status_code, entity", TEST_CASES)
def test_lookup(
  status_code: int,
  entity:      models.VehicleEntity,
) -> None:
  pass
# {..}
