import os
import json
import traceback
import statistics
import openai
from typing import Any, Dict
from dotenv import dotenv_values

from .prompt import better_answers_prompt
from .input import BetterAnswersInput
from .output import SearchDocument, BetterAnswersOutput

config = {
    **dotenv_values(os.path.join(os.path.dirname(__file__), '..', '.env')),
    **os.environ,
}

openai.api_key = config.get('OPENAI_API_KEY')


def handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    try:
        uid = event.get('requestContext', {}).get(
            'authorizer', {}).get('principalId')

        body = event.get('body')

        if body is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'please provide POST body'}),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }

        body = json.loads(body)
        input = BetterAnswersInput(**body)

        search_response = openai.Engine(input.search_model).search(
            file=input.file,
            query=input.question,
            max_rerank=input.max_rerank,
            return_metadata=input.return_metadata,
        ).to_dict_recursive()

        scores = [d.get('score', 0) for d in search_response.get('data', [])]
        mean = statistics.mean(scores)
        stdev = statistics.stdev(scores)

        filtered_documents = filter(
            lambda d: (d.get('score', 0) - mean) / stdev > input.z_threshold,
            search_response.get('data', []),
        ) if input.z_threshold is not None else search_response.get('data', [])

        selected_documents = list(map(
            lambda d: SearchDocument(**d, z_val=(d.get('score', 0) - mean) / stdev),
            sorted(
                filtered_documents,
                key=lambda d: d.get('score', 0),
            ),
        ))

        if len(selected_documents) == 0:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'no matching documents found'}),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }

        prompt, idx = better_answers_prompt(
            input.model,
            input.max_tokens,
            input.question,
            selected_documents,
            examples=input.examples,
            examples_context=input.examples_context,
        )

        completion_response = openai.Completion.create(
            engine=input.model,
            prompt=prompt,
            max_tokens=input.max_tokens,
            temperature=input.temperature,
            n=input.n,
            stop=input.stop,
            logprobs=input.logprobs,
            logit_bias=input.logit_bias if input.logit_bias is not None else {},
        ).to_dict_recursive()

        better_answers_response = BetterAnswersOutput(
            # TODO: fix response for situations when logprobs and logit_bias is configured
            answers=[a.get('text', '').strip() for a in completion_response.get('choices', [])],
            completion=completion_response.get('id'),
            file=input.file,
            model=completion_response.get('model'),
            prompt=prompt if input.return_prompt else None,
            search_model=input.search_model,
            selected_documents=[SearchDocument(**d.dict(exclude={'metadata'})) if not input.return_metadata else d for d in selected_documents[idx:]],
        )

        return {
            'statusCode': 200,
            'body': better_answers_response.json(),
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
