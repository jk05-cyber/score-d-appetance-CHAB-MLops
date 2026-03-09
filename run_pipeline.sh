#!/bin/bash

# Full ML Pipeline Execution Script
# Runs: Tests → Training → Scoring → Drift Monitoring

set -e  # Exit on error

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

export PYTHONPATH="$PROJECT_DIR"

echo "=========================================="
echo "🚀 STARTING FULL ML PIPELINE"
echo "=========================================="
echo ""

# Step 1: Run Tests
echo "📋 STEP 1: Running Unit Tests..."
python3 -m pytest tests/ -q --tb=no
echo "✅ Tests passed!"
echo ""

# Step 2: Train Models
echo "📈 STEP 2: Training Models..."
python3 pipelines/training_flow.py
echo "✅ Training complete!"
echo ""

# Step 3: Score Clients
echo "🎯 STEP 3: Scoring Clients..."
python3 pipelines/scoring_flow.py
echo "✅ Scoring complete!"
echo ""

# Step 4: Generate Drift Report
echo "📊 STEP 4: Generating Drift Report..."
python3 << 'EOFPYTHON'
from src.monitoring.drift_report import generate_report
import os
os.makedirs("src/data/reports", exist_ok=True)
generate_report("src/data/processed/dataset.csv", "src/data/scored/batch_scores.csv", "src/data/reports/drift_report.csv")
print("✅ Drift report generated!")
EOFPYTHON
echo ""

# Step 5: Display Results
echo "=========================================="
echo "🎉 PIPELINE EXECUTION COMPLETE!"
echo "=========================================="
echo ""
echo "📌 Generated Artifacts:"
echo "   • $(wc -l < src/data/processed/dataset.csv) rows in processed dataset"
echo "   • $(wc -l < src/data/scored/batch_scores.csv) rows in scored output"
echo "   • Drift report: src/data/reports/drift_report.csv"
echo ""
echo "🚀 To start the API, run:"
echo "   uvicorn src.api.app:app --host 0.0.0.0 --port 8000"
echo ""
echo "📖 View API docs at: http://localhost:8000/docs"
echo ""
