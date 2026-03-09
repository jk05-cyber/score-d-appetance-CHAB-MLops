# 🚀 Quick Start - Run Full Pipeline

## Option 1: Bash Script (Recommended)
```bash
./run_pipeline.sh
```
✅ Runs everything in one command  
✅ Shows progress with clear steps  
✅ Handles errors automatically  

## Option 2: Make Command
```bash
# Full pipeline without API
make pipeline

# Full pipeline with API in background
make all
```

## Option 3: Python One-Liner
```bash
python3 -c "import subprocess, sys; subprocess.run(['pytest', 'tests/', '-q'], check=True) or subprocess.run(['python3', 'pipelines/training_flow.py'], check=True) or subprocess.run(['python3', 'pipelines/scoring_flow.py'], check=True)"
```

## Option 4: Manual Chaining
```bash
pytest tests/ && python pipelines/training_flow.py && python pipelines/scoring_flow.py
```

## ✨ Recommended: Full Pipeline with API

```bash
# Terminal 1: Run full pipeline
./run_pipeline.sh

# Terminal 2: Start API server
uvicorn src.api.app:app --host 0.0.0.0 --port 8000

# Terminal 3: Test API
curl http://localhost:8000/health
```

---

## 📊 What Each Step Does

### Step 1: Unit Tests (30 sec)
- Validates all modules work correctly
- Tests features, training, and API

### Step 2: Training (2 min)
- Builds dataset from RC/PC/MOUVEMENT data
- Trains Logistic Regression & Random Forest
- Registers best model in MLflow

### Step 3: Scoring (10 sec)
- Loads trained model
- Generates predictions for all 220,000 clients
- Outputs: `src/data/scored/batch_scores.csv`

### Step 4: Drift Monitoring (5 sec)
- Compares training vs. scoring data distributions
- Outputs: `src/data/reports/drift_report.csv`

---

## 🛠️ Troubleshooting

**If script fails to run:**
```bash
chmod +x ./run_pipeline.sh
./run_pipeline.sh
```

**If you need to install dependencies first:**
```bash
pip install -r requirements.txt
./run_pipeline.sh
```

**To run individual steps:**
```bash
make test      # Run tests only
make train     # Run training only
make score     # Run scoring only
make drift     # Run drift monitoring only
make api       # Start API server
```

---

## 📈 Expected Output

```
==========================================
🚀 STARTING FULL ML PIPELINE
==========================================

📋 STEP 1: Running Unit Tests...
✅ Tests passed!

📈 STEP 2: Training Models...
✅ Training complete!

🎯 STEP 3: Scoring Clients...
✅ Scoring complete!

📊 STEP 4: Generating Drift Report...
✅ Drift report generated!

==========================================
🎉 PIPELINE EXECUTION COMPLETE!
==========================================

📌 Generated Artifacts:
   • 220001 rows in processed dataset
   • 220001 rows in scored output
   • Drift report: src/data/reports/drift_report.csv

🚀 To start the API, run:
   uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

---

## 🎯 Total Execution Time
**~3 minutes** from start to finish
