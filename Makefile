-include .env
export

create-jwt:
	poetry run python ./scripts/create_jwt.py

split-sentences:
	poetry run python ./functions/split_sentences.py
