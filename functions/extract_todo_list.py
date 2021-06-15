import os
import json
import traceback
from typing import Any, Dict
from dotenv import dotenv_values
from aws_lambda_powertools.utilities.typing import LambdaContext
import openai
import dateparser

# in lambdas, try to use more absolute package import
from functions.prompts import extract_todo_list_prompt

config = {
    **dotenv_values(os.path.join(os.path.dirname(__file__), '..', '.env')),
    **os.environ,
}

openai.api_key = config.get('OPENAI_API_KEY')


def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    try:
        body = event.get('body')

        if body is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'please provide POST body'}),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }

        message = json.loads(body).get('message')

        if message is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'please provide message in body JSON'}),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }

        response = openai.Completion.create(
            engine='davinci-instruct-beta',
            prompt=extract_todo_list_prompt(message),
            max_tokens=256,
            temperature=0.3,
            stop=['####'],
        )

        todo_list = response.get('choices', {})[0].get('text')

        if todo_list is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'no sentences produced'}),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }

        # do this to ensure valid json
        todo_list = json.loads(todo_list)
        # TODO: process time as needed by Siri

        return {
            'statusCode': 200,
            'body': json.dumps({'todo_list': todo_list}),
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
