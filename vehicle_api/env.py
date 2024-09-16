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

COLLECTION_NAME = _env_var("COLLECTION_NAME")
MONGODB_URI     = _env_var("MONGODB_URI")

LIMIT = _env_var("LIMIT", int, 50)

# {...}
