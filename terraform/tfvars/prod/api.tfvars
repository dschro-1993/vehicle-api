tags = {
  COST_CENTER = "001" # => Just as an example!
  # {...}
}

env_vars = {
  POWERTOOLS_SERVICE_NAME = "serverless-airline"
  POWERTOOLS_LOG_LEVEL    = "WARNING"

  COLLECTION_NAME       = "vehicles_prod"
  MONGODB_URI_SSM_PARAM = "prod_MONGODB_URI"
  ENV                   = "prod"
  # {...}
}

env = "prod"

# {...}
