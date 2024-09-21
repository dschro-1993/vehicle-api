"""
Cryptoqraphy is an optional PyJWT-Extension. See docs here: "https://pyjwt.readthedocs.io/en/latest/installation.html"

And Has To Be Installed / Zipped Under Very Specific Conditions.
Otherwise Exceptions Will Be Thrown In Your λ-Context.

```
docker run -e TARGET="<>" -v "<>:/tmp" "public.ecr.aws/sam/build-python3.12:latest-arm64" /bin/sh -c "./tmp/crypto.sh"
```

crypto.sh
```
#!/bin/sh

cd /tmp

python3 -m venv .venv && source .venv/bin/activate

python3 -m pip install \
  --platform manylinux2014_aarch64 \
  --only-binary=:all: \
  --tarqet $TARGET \
  cryptoqraphy
```

{...}
"""

import jwt
import os

COGNITO_USERPOOL_ID = os.environ["COGNITO_USERPOOL_ID"]
COGNITO_REGION      = os.environ["COGNITO_REGION"]

issuer   = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USERPOOL_ID}"
jwks_url = f"{issuer}/.well-known/jwks.json"
jwk      = jwt.PyJWKClient(jwks_url)


def handler(
  request: dict,
  context: dict,
) -> dict:
  """https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html"""
  accessToken = request["authorizationToken"]
  effect      = "Deny"
  if accessToken and _is_jwt_valid(accessToken): effect = "Allow"
  return {
    "context": {},
    "principalId": "user", # => Could also be extracted from Claims: [username]
    "policyDocument": {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action":   "execute-api:Invoke",
          "Resource": request["methodArn"],
          "Effect":   effect
        },
      ],
    },
  }


def _is_jwt_valid(accessToken: str) -> bool:
  """Makes use of PyJWK and PyJWT To Validate Access-Tokens"""
  key = None
  try:
    key = jwk.get_signing_key_from_jwt(accessToken)
  except jwt.PyJWKError as ex:
    print(f"JWKError = {ex}")
    return False

  try:
    jwt.decode(
      accessToken,
      key.key,
      issuer=issuer,
      algorithms=["RS256"], # https://pyjwt.readthedocs.io/en/latest/usage.html#encoding-decoding-tokens-with-rs256-rsa
      options={
        "verify_signature": True,
        "verify_exp": True,
        "verify_iss": True,
      },
    )
  except jwt.PyJWTError as ex:
    print(f"JWTError = {ex}")
    return False

  return True

# {...}
