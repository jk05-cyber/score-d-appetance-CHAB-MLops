install:
	python -m pip install -r requirements.txt

train:
	python -m pipelines.training_flow

score:
	python -m pipelines.scoring_flow

test:
	pytest -q

api:
	uvicorn src.api.app:app --reload

lint:
	flake8 src tests
