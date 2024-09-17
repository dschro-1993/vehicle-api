tags = {
  COST_CENTER = "002" # => Just as an example!
  # {...}
}

env_vars = {
  
  POWERTOOLS_SERVICE_NAME = "serverless-airline-booking"
  POWERTOOLS_LOG_LEVEL    = "DEBUG"

  POWERTOOLS_PARAMETERS_SSM_DECRYPT = !false
  POWERTOOLS_PARAMETERS_MAX_AGE     = 300

  MONGODB_USERNAME_SSM_PARAMETER = "MONGODB_USERNAME"
  MONGODB_PASSWORD_SSM_PARAMETER = "MONGODB_PASSWORD"
  MONGODB_ENDPOINT               = "<>"
  COLLECTION                     = "vehicles_qa"
  ENV                            = "qa"
  # {...}
}

env = "qa"

# {...}
