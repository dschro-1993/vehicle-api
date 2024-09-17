tags = {
  COST_CENTER = "002" # => Just as an example!
  # {...}
}

env_vars = {
  POWERTOOLS_SERVICE_NAME = "serverless-airline"
  POWERTOOLS_LOG_LEVEL    = "DEBUG"

  COLLECTION_NAME       = "vehicles_qa"
  MONGODB_URI_SSM_PARAM = "qa_MONGODB_URI"
  ENV                   = "qa"
  # {...}
}

env = "qa"

# {...}
