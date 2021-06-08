try:
  import unzip_requirements
except ImportError:
  pass

import os
import json
from typing import Any, Dict
from dotenv import dotenv_values
from jwcrypto import jwk, jwt
from aws_lambda_powertools.utilities.typing import LambdaContext

config = {
    **dotenv_values(os.path.join(os.path.dirname(__file__), '..', '.env')),
    **os.environ,
}

signing_key = jwk.JWK.from_json(config.get('JWT_SIGNING_KEY'))

def generatePolicy(principalId, effect, methodArn):
    authResponse = {}
    authResponse['principalId'] = principalId

    if effect and methodArn:
        policyDocument = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'FirstStatement',
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': methodArn
                }
            ]
        }

        authResponse['policyDocument'] = policyDocument

    return authResponse

def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    try:
        # test the JWT
        token = str(event['authorizationToken']).replace('jwt ', '')
        print('jwt token', token)
        decrypted = jwt.JWT(key=signing_key, jwt=token)
        print('jwt claims', decrypted.claims)

        # Get principalId from idInformation
        principalId = json.loads(decrypted.claims).get('uid')
    except:
        # Deny access if the token is invalid
        return generatePolicy(None, 'Deny', event['methodArn'])

    return generatePolicy(principalId, 'Allow', event['methodArn'])

if __name__ == '__main__':
    print(signing_key.export_public())
