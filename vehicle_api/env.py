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
MONGODB_ENDPOINT               = _env_var("MONGODB_ENDPOINT")
MONGODB_USERNAME_SSM_PARAMETER = _env_var("MONGODB_USERNAME_SSM_PARAMETER")
MONGODB_PASSWORD_SSM_PARAMETER = _env_var("MONGODB_PASSWORD_SSM_PARAMETER")

COLLECTION = _env_var("COLLECTION")

LIMIT = _env_var("LIMIT", int, 100)

ENV = _env_var("ENV")

# {...}
