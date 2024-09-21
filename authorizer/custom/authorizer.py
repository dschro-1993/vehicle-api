import jwt
import os

COGNITO_USERPOOL_ID = os.environ["COGNITO_USERPOOL_ID"]
COGNITO_REGION      = os.environ["COGNITO_REGION"]

issuer   = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USERPOOL_ID}"
jwks_url = f"{issuer}/.well-known/jwks.json"
jwks     = jwt.PyJWKClient(jwks_url)

def is_valid(_jwt: str) -> bool:
  """Todo"""
  key = None
  try:
    key = jwks.get_signing_key_from_jwt(_jwt)
  except jwt.PyJWKError as ex:
    print(f"JWKError = {ex}")
    return False

  try:
    jwt.decode(
      _jwt,
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
