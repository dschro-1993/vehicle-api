"""DB for Vehicle-API"""

import os

from pymongo import MongoClient

from aws_lambda_powertools import (
  Logger,
  Tracer,
)

logger = Logger()
tracer = Tracer()

class DB:
  """
  For docs please see here:
  https://www.mongodb.com/docs/languages/python/pymongo-driver/current/
  """
  def __init__(self) -> None:
    self.db = (
      MongoClient(f"{os.environ["MONGODB_URI"]}?uuidRepresentation=standard")
      ["db"] # Todo
    )

  @staticmethod
  def _load_cursor() -> list[dict]:
    pass

  @tracer.capture_method()
  def search(self, collection_name: str, filter: dict, aggregation: dict, sort: list[tuple[str, int]], limit: int, skip: int) -> list[dict]:
    """
    For docs please see here:
    https://www.mongodb.com/docs/languages/python/pymongo-driver/current/read/retrieve/#find-documents
    """
    try:
      rs = self.db[collection_name].find(filter, aggregation, sort=sort, limit=limit, skip=skip)
      logger.debug(rs)
      # We could also return a Cursor/Iterator here...
      return  list(rs)
    except Exception as ex:
      logger.error(ex)
      raise ex
      # {...}

  @tracer.capture_method()
  def search_one(self, collection_name: str, filter: dict) -> None | dict:
    """
    For docs please see here:
    https://www.mongodb.com/docs/languages/python/pymongo-driver/current/read/retrieve/#find-documents
    """
    try:
      rs = self.db[collection_name].find_one(filter)
      logger.debug(rs)
      return rs
    except Exception as ex:
      logger.error(ex)
      raise ex
      # {...}

  @tracer.capture_method()
  def update_one(self, collection_name: str, filter: dict, update: dict) -> None | dict:
    """
    For docs please see here:
    https://www.mongodb.com/docs/languages/python/pymongo-driver/current/write/update/#update-one-document
    """
    try:
      rs = self.db[collection_name].find_one_and_update(
        filter,
        {"$set": update},
        return_document = True,
      )
      logger.debug(rs)
      return rs
    except Exception as ex:
      logger.error(ex)
      raise ex
      # {...}

  @tracer.capture_method()
  def insert_one(self, collection_name: str, entity: dict) -> None:
    """
    For docs please see here:
    https://www.mongodb.com/docs/languages/python/pymongo-driver/current/write/insert/#insert-one-document
    """
    try:
      self.db[collection_name].insert_one(entity)
      logger.debug(
        "In Collection %s created an Entity: %s",
        collection_name,
        entity,
      )
    except Exception as ex:
      logger.error(ex)
      raise ex
      # {...}

  @tracer.capture_method()
  def delete_one(self, collection_name: str, filter: dict) -> None:
    """
    For docs please see here:
    https://www.mongodb.com/docs/languages/python/pymongo-driver/current/write/delete/#delete-one-document
    """
    try:
      self.db[collection_name].delete_one(filter)
      logger.debug(
        "In Collection %s deleted an Entity: %s",
        collection_name,
        filter,
      )
    except Exception as ex:
      logger.error(ex)
      raise ex
      # {...}

# {...}
