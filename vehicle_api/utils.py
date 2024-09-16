"""Utilities for Vehicle-API"""

from botocore.config import Config

boto_config = Config(
  # proxies = {...},
  # proxies_config = {...},
  # retries = {"mode": "standard"},
  tcp_keepalive = True,
  # {...}
)

# {...}
