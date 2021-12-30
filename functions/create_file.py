import os
import json
import traceback
import openai
import boto3
from typing import Any, Dict
from dotenv import dotenv_values

config = {
    **dotenv_values(os.path.join(os.path.dirname(__file__), '..', '.env')),
    **os.environ,
}

openai.api_key = config.get('OPENAI_API_KEY')

def handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    try:
        # uid = event.get('requestContext', {}).get(
        #     'authorizer', {}).get('principalId')

        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        s3_resource = boto3.resource('s3')
        s3_object = s3_resource.Object(bucket, key)
        s3_response = s3_object.get()

        filename = key.split('/')[-1]
        filename_parts = filename.split('.')

        if len(filename_parts) != 3:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'invalid filename format'}),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }

        file_response = openai.File.create(file=s3_response['Body'], purpose=filename_parts[1])
        file_id = file_response.get('id', '')
        new_s3_object = s3_resource.Object(bucket, f'{file_id}')
        new_s3_object.copy_from(CopySource=dict(Bucket=bucket, Key=key))
        s3_object.delete()

        return {
            'statusCode': 200,
            'body': json.dumps(file_response),
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
