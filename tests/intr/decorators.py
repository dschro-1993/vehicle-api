from typing import Callable

import contextlib
import functools
import boto3
import os

ENDPOINT = os.environ.get("ENDPOINT", "HTTP://127.0.0.1:8000")
DDBTABLE = os.environ.get("DDBTABLE", "Vehicles")

dynamodb = boto3.client("dynamodb", endpoint_url=ENDPOINT)

def make_Table(test_func: Callable) -> None:
  """
  1. Delete-Table (if existent)
  2. Create-Table
  3. Invoke test-func
  """
  @functools.wraps(test_func) # => To make custom Decorator work with Pytest
  def func(*args, **kwargs):
    # Suppress Exception on 1st test
    with contextlib.suppress(Exception): dynamodb.delete_table(TableName=DDBTABLE)

    dynamodb.create_table(
      TableName   = DDBTABLE,
      BillingMode = "PAY_PER_REQUEST",
      KeySchema = [
        {
          "AttributeName": "id",
          "KeyType":       "HASH"
        }
      ],
      AttributeDefinitions = [
        {
          "AttributeName": "id",
          "AttributeType": "S"
        }
      ]
    )
    test_func(*args, **kwargs)

  return func
