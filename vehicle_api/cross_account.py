"""Utility To fetch and cache AWS Cross-Account Credentials"""

import time
import boto3

from aws_lambda_powertools import (
  Logger
)

# Global dict to store all cached Credentials
cached_credentials_map = {}

account_to_role_map = {
  "<account_id_1>": "<role_arn_1>",
  "<account_id_2>": "<role_arn_2>",
  # {...}
}

client = boto3.client("sts")

logger = Logger()

def assume_role_for_account_id(account_id: str) -> dict | None:
  """
  Assumes IAM-Role based on ARN, using given "account_id".
  Returns AWS Credentials as dict or None if "account_id"
  was unknown!
  """
  if account_id in account_to_role_map:

    if cached_credentials_map.get(account_id, {}).get("Expiration", 0) > time.time():
      logger.debug("Credentials reused")
      return cached_credentials_map[account_id]

    try:
      my_role = account_to_role_map[account_id]
      resps = client.assume_role(
        DurationSeconds=900, # 15-Minutes => Can also be injected as an Env-Variable!
        RoleSessionName=f"λSession-{account_id}",
        RoleArn=my_role,
      )

      creds = resps["Credentials"]
      cached_credentials_map[account_id] = creds

      # 1-Minute Buffer
      cached_credentials_map[account_id]["Expiration"] = (
        creds["Expiration"].timestamp() - 60
      )
      return creds
    except Exception as ex:
      logger.debug(ex)
      raise ex
    # {...}
# {...}
