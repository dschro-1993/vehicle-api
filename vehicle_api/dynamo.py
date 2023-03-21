"""Repository for Vehicle-API"""

import os
import boto3

from typing import Union
from models import Vehicle

from aws_lambda_powertools import Logger
logger = Logger()

class Dynamo:
  """Dynamo-Class"""
  def __init__(self) -> None:
    """
    https://docs.aws.amazon.com/cli/latest/reference/dynamodb
    """
    ENDPOINT = os.environ.get("ENDPOINT", None)
    DDBTABLE = os.environ.get("DDBTABLE", None)

    # config=Config(tcp_keepalive=True)
    self.table = (
      boto3.resource("dynamodb", endpoint_url=ENDPOINT)
      .Table(DDBTABLE)
    )

  def delete(self, id: str) -> None:
    """
    https://docs.aws.amazon.com/cli/latest/reference/dynamodb/delete-item.html
    """
    self.table.delete_item(Key={"id": id})
    logger.info("Deleted Vehicle of following id: %s", id)

  def put(self, vehicle: Vehicle) -> None:
    """
    https://docs.aws.amazon.com/cli/latest/reference/dynamodb/put-item.html
    """
    item = vehicle.dict()
    self.table.put_item(Item=item)
    logger.info("Created Vehicle: %s", item)

  def get(self, id: str) -> Union[Vehicle, None]:
    """
    https://docs.aws.amazon.com/cli/latest/reference/dynamodb/get-item.html
    """
    json = (
      self.table
      .get_item(Key={"id": id})
      .get("Item" , None)
    )
    return (
      Vehicle(**json) if json != None
      else None
    )
