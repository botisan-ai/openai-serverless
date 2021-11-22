-include .env
export

create-jwt:
	pipenv run python ./scripts/create_jwt.py

sign-jwt:
	pipenv run python ./scripts/sign_jwt.py $(user)

authorizer:
	pipenv run python ./functions/authorizer.py

split-sentences:
	pipenv run python ./functions/split_sentences.py

openai-api:
	pipenv run openai api $(args)

list-models:
	pipenv run openai api models.list

delete-model:
	pipenv run openai api models.delete -i $(model)

local:
	yarn serverless offline start $(args)

deploy:
	yarn serverless deploy $(args)
