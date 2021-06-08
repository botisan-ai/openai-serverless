import os
import json
import traceback
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

        message = json.loads(body).get('message')

        if message is None:
            return {
                'statusCode': 400,
                'body': json.dumps({ 'message': 'please provide sentence in body JSON' }),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }

        prompt = f'''Extract the people names from the message. Put one name per line.
####
Message:
I am actually the assistant here with Justin Hahn so I'm here to answer any questions you might have!
People names:
Justin Hahn
####
Message:
My name is Raiya and I work for Karie Milford at Milford Real Estate.
People names:
Raiya
Karie Milford
####
Message:
I will pass this on to my associate, Shane Hamilton, right away and let them coordinate a time with you
People names:
Shane Hamilton
####
Message:
Hugo Avalos will be in touch with you at (323) 548-1370
People names:
Hugo Avalos
####
Message:
{message}
People names:'''
        response = openai.Completion.create(
            engine='curie-instruct-beta',
            prompt=prompt,
            max_tokens=256,
            temperature=0.5,
            stop=['####'],
        )

        people_names = response.get('choices', {})[0].get('text')

        if people_names is None:
            return {
                'statusCode': 400,
                'body': json.dumps({ 'message': 'no sentences produced' }),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }

        people_names = list(filter(lambda s: s.strip(), str(people_names).split('\n')))

        return {
            'statusCode': 200,
            'body': json.dumps({ 'people_names': people_names }),
            'headers': {
                'Content-Type': 'application/json',
            },
        }
    except Exception:
        traceback.print_exc()
        return {
            'statusCode': 400,
            'body': json.dumps({ 'message': 'error occurred, please check logs' }),
            'headers': {
                'Content-Type': 'application/json',
            },
        }

if __name__ == '__main__':
    print(config)
