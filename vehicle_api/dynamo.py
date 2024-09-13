"""Dynamo for Vehicle-API"""

import boto3
import utils

from aws_lambda_powertools import (
  Logger,
  Tracer,
)

logger = Logger()
tracer = Tracer()

class Dynamo:
  """Dynamo-Class for wrapping and simplifying boto3-Calls"""
  def __init__(self) -> None:
    """
    Todo: Add Env-Var for Endpoint-Url (Int-Tests)
    https://hub.docker.com/r/amazon/dynamodb-local
    """
    self.dynamo = boto3.resource("dynamodb", config=utils.boto_config)

  def delete(self, table_name: str, keys: dict) -> None:
    """
    For docs please see here:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/delete_item.html
    """
    table = self.dynamo.Table(table_name)
    table.delete_item(Key = keys)
    logger.debug(
      "In Table '%s' deleted Item of Keys: %s",
      table_name,
      keys,
    )

  def create(self, table_name: str, item: dict) -> None:
    """
    For docs please see here:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/put_item.html
    """
    table = self.dynamo.Table(table_name)
    table.put_item(Item = item)
    logger.debug(
      "In Table '%s' created/updated Item: %s",
      table_name,
      item,
    )

  def lookup(self, table_name: str, keys: dict) -> None | dict:
    """
    For docs please see here:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/get_item.html
    """
    table = self.dynamo.Table(table_name)
    item  = (
      table
      .get_item(Key = keys)
      .get("Item")
    )
    if item is None:
      return None
    logger.debug(
      "In Table '%s' fetched Item of Keys: %s",
      table_name,
      keys,
    )
    return (
      item
    )
