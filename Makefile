-include .env
export

create-jwt:
	poetry run python ./scripts/create_jwt.py

sign-jwt:
	poetry run python ./scripts/sign_jwt.py $(user)

authorizer:
	poetry run python ./functions/authorizer.py

split-sentences:
	poetry run python ./functions/split_sentences.py

local:
	yarn serverless offline start $(args)

deploy:
	yarn serverless deploy $(args)
