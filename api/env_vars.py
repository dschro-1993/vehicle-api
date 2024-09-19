import os

from typing import (
  TypeVar,
  Type,
)

T = TypeVar("T")

def _env_var(key: str, typecast: Type[T] = str, fallback: T = None) -> T:
  if key in os.environ:
    return typecast(os.environ[key])

  if fallback is None:
    raise ValueError(f"No Value was found in Env-Vars for: 'Key={key}', and no Fallback was provided!")

  return fallback
# {...}

#  ---

# DB_USERNAME_SSM_PARAMETER = _env_var("DB_USERNAME_SSM_PARAMETER") # => Fix VPC Interface-Endpoint
# DB_PASSWORD_SSM_PARAMETER = _env_var("DB_PASSWORD_SSM_PARAMETER")

COLLECTION_NAME = _env_var("COLLECTION_NAME")
DB_ENDPOINT     = _env_var("DB_ENDPOINT")
DB_USERNAME     = _env_var("DB_USERNAME")
DB_PASSWORD     = _env_var("DB_PASSWORD")

LIMIT_MAXIMUM = _env_var("LIMIT_MAXIMUM", int, 10000)
LIMIT         = _env_var("LIMIT", int, 100)

# ENV = _env_var("ENV")

# {...}
