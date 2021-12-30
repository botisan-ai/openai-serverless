# OpenAI Serverless

A Stack for managing OpenAI API access using Serverless Framework against AWS. This is useful for exposing your custom OpenAI API usage to the public or run experiments.

## Features

- [x] JWT Authentication (multi-user support)
  - [ ] Usage counting and segregation for each JWT user (In Progress)
- [x] Improved Answers Endpoint (`/better_answers`)
- [x] File uploads via S3
  - [ ] Queued file uploads (Planned)
## Prerequisites

- NodeJS LTS
- yarn
- pyenv
- Pipenv
- make
- Docker (for building dependencies during deployment)

## Install

```shell
# install serverless dependencies
yarn install
# install python dependencies
pipenv install
```

## Env Vars

Please check `.env.example`. Copy to `.env` and add the OpenAI API Key.

Run `make create-jwt` to create the JWK for signing. Put that in to `.env`.

Run `make sign-jwt user="<username>"` to get a signed JWT for requests.

## How to test locally

```shell
make local args="--stage dev"
```

## How to deploy

First make sure we have the right AWS profile set up, it is best to inject keys via `AWS_PROFILE` env var. (Put into `.env` is fine).

```shell
make deploy
```

## How to make requests

For example, with `/better_answers`:

```shell
curl --request POST \
  --url http://localhost:3000/dev/better_answers \
  --header 'Authorization: jwt <jwt_token>' \
  --header 'Content-Type: application/json' \
  --data '{
	"file": "file-xxxx",
	"question": "Can I update my User ID?",
	"temperature": 0,
	"search_model": "babbage",
	"model": "davinci-instruct-beta-v3",
	"examples_context": "In 2017, U.S. life expectancy was 78.6 years.",
	"examples": [["What is human life expectancy in the United States?","78 years."]],
	"max_tokens": 32,
	"max_rerank": 50,
	"z_threshold": 1,
	"stop": ["\n", "===", "<|endoftext|>"]
}'
```

## Current Methods

TODO

## License

[MIT](./LICENSE)
