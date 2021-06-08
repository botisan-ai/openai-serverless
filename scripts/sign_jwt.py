import os
import sys
from dotenv import dotenv_values
from jwcrypto import jwk, jwt

config = {
    **dotenv_values(os.path.join(os.path.dirname(__file__), '..', '.env')),
    **os.environ,
}

signing_key = jwk.JWK.from_json(config.get('JWT_SIGNING_KEY'))

print('signing JWT for user', sys.argv[1])

token = jwt.JWT(header={'alg': 'HS256'}, claims={'uid': sys.argv[1]})

token.make_signed_token(signing_key)

print(token.serialize())
