# OpenAI Serverless

A Stack for managing OpenAI API access using Serverless Framework against AWS.

## Prerequisites

- NodeJS LTS
- yarn
- pyenv
- Poetry
- make

## Install

```
yarn
poetry install
```

## Env Vars

Please check `.env.example`. Copy to `.env` and add the OpenAI API Key.

Run `make create-jwt` to create the JWK for signing. Put that in to `.env`.

Run `make sign-jwt user="<username>"` to get a signed JWT for requests.

## How to run locally

```
make local args="--stage dev"
```

## How to deploy

First make sure we have the right AWS profile set up, it is best to inject keys via `AWS_PROFILE` env var. (Put into `.env` is fine).

```
make deploy
```

## How to make requests

For example, with `/split_sentences`:

```
curl --request POST \
  --url http://localhost:3000/dev/split_sentences \
  --header 'Authorization: jwt <jwt_token>' \
  --header 'Content-Type: application/json' \
  --data '{
	"sentence": "This is a sentence splitter that can split sentences into its own line. Please feel free to try it out!"
}'
```
