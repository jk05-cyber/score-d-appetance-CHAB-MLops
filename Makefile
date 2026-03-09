install:
	python3 -m pip install -r requirements.txt

train:
	PYTHONPATH=. python3 -m pipelines.training_flow

score:
	PYTHONPATH=. python3 -m pipelines.scoring_flow

test:
	python3 -m pytest tests/ -q --tb=no

api:
	PYTHONPATH=. python3 -m uvicorn src.api.app:app --reload

lint:
	python3 -m flake8 src tests

drift:
	PYTHONPATH=. python3 -c "from src.monitoring.drift_report import generate_report; import os; os.makedirs('src/data/reports', exist_ok=True); generate_report('src/data/processed/dataset.csv', 'src/data/scored/batch_scores.csv', 'src/data/reports/drift_report.csv'); print('✅ Drift report generated')"

pipeline: test train score drift

all: test train score drift api

.PHONY: install train score test api lint drift pipeline all
