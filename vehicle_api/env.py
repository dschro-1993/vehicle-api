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
MONGODB_URI_SSM_PARAM = _env_var("MONGODB_URI_SSM_PARAM")
COLLECTION_NAME       = _env_var("COLLECTION_NAME")

LIMIT = _env_var("LIMIT", int, 50)

ENV = _env_var("ENV")

# {...}
