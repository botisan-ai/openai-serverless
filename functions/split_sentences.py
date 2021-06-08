import os
import json
from typing import Any, Dict
from dotenv import dotenv_values
from aws_lambda_powertools.utilities.typing import LambdaContext
import openai

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
                'body': json.dumps({ 'message': 'please provide POST body' }),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }

        sentence = json.loads(body).get('sentence')

        if sentence is None:
            return {
                'statusCode': 400,
                'body': json.dumps({ 'message': 'please provide sentence in body JSON' }),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }

        prompt = f'''Split the message into individual sentences. Put each sentence into its own line. Keep the original punctuations as much as possible.
####
Message:
Hi, my name is Simon. I am working on a sentence splitter powered by OpenAI
Sentences:
Hi, my name is Simon.
I am working on a sentence splitter powered by OpenAI
####
Message:
{sentence}
Sentences:'''
        response = openai.Completion.create(
            engine='curie-instruct-beta',
            prompt=prompt,
            max_tokens=256,
            temperature=0.3,
            stop=['####'],
        )

        sentences = response.get('choices', {})[0].get('text')

        if sentences is None:
            return {
                'statusCode': 400,
                'body': json.dumps({ 'message': 'no sentences produced' }),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }

        sentences = list(filter(lambda s: s.strip(), str(sentences).split('\n')))

        return {
            'statusCode': 200,
            'body': json.dumps({ 'sentences': sentences }),
            'headers': {
                'Content-Type': 'application/json',
            },
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({ 'message': 'error occurred, please check logs' }),
            'headers': {
                'Content-Type': 'application/json',
            },
        }

if __name__ == '__main__':
    print(config)
