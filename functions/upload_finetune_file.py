import os
import json
import uuid
import traceback
import boto3
from typing import Any, Dict
from dotenv import dotenv_values

config = {
    **dotenv_values(os.path.join(os.path.dirname(__file__), '..', '.env')),
    **os.environ,
}

BUCKET_NAME = config.get('BUCKET_NAME')


def handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    try:
        uid = event.get('requestContext', {}).get(
            'authorizer', {}).get('principalId')

        s3_client = boto3.client('s3')

        object_key = f'{uid}/{str(uuid.uuid4())}.jsonl'

        response = s3_client.generate_presigned_post(BUCKET_NAME, object_key)

        return {
            'statusCode': 200,
            'body': json.dumps(response),
            'headers': {
                'Content-Type': 'application/json',
            },
        }
    except Exception:
        traceback.print_exc()
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'error occurred, please check logs'}),
            'headers': {
                'Content-Type': 'application/json',
            },
        }


if __name__ == '__main__':
    print(config)
