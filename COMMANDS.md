# 🚀 Pipeline Execution Commands

## Quick Reference

### Absolute Quickest (1 Command)
```bash
make pipeline
```

---

## All Options

### 1. **Make (Recommended)** 🔨
```bash
# Pipeline without API
make pipeline

# Full pipeline with API  
make all
```

### 2. **Bash Script** 🐚
```bash
./run_pipeline.sh
```

### 3. **Direct Command Chain** ⚡
```bash
pytest tests/ -q && PYTHONPATH=. python3 -m pipelines.training_flow && PYTHONPATH=. python3 -m pipelines.scoring_flow
```

### 4. **Individual Commands** 📦
```bash
# Just tests
make test

# Just training
make train

# Just scoring
make score

# Just drift monitoring
make drift

# Start API
make api
```

---

## What Runs in Each Command

| Command | Tests | Train | Score | Drift |
|---------|-------|-------|-------|-------|
| `make pipeline` | ✅ | ✅ | ✅ | ✅ |
| `make all` | ✅ | ✅ | ✅ | ✅ + API |
| `./run_pipeline.sh` | ✅ | ✅ | ✅ | ✅ |
| `make test` | ✅ | - | - | - |
| `make train` | - | ✅ | - | - |
| `make score` | - | - | ✅ | - |
| `make drift` | - | - | - | ✅ |

---

## Step-by-Step Breakdown

**Step 1: Unit Tests** (~30 sec)
- Validates all code modules
- Ensures data pipelines work
- 6 tests pass

**Step 2: Training** (~2 min)
- Loads raw data (RC, PC, MOUVEMENT)
- Engineers features
- Trains 2 models (LogReg, RF)
- Best: Logistic Regression (AUC: 0.604)

**Step 3: Scoring** (~10 sec)
- Loads trained model
- Scores 220,000 clients
- Output: `src/data/scored/batch_scores.csv`

**Step 4: Drift Monitoring** (~5 sec)
- Compares train vs scored distributions
- Output: `src/data/reports/drift_report.csv`

---

## Complete Workflow

```bash
# Terminal 1: Run full pipeline (~3 min)
make pipeline

# After it completes, Terminal 2: Start API
make api

# Terminal 3: Test the API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/docs
```

---

## Outputs Created

After running any pipeline:
- ✅ `src/data/processed/dataset.csv` (220K rows)
- ✅ `src/data/scored/batch_scores.csv` (predictions for 220K clients)
- ✅ `src/data/reports/drift_report.csv` (monitoring)
- ✅ `mlruns/` (MLflow experiment tracking)

---

## Troubleshooting

**If PYTHONPATH error occurs:**
```bash
export PYTHONPATH=/path/to/project
make pipeline
```

**If dependencies missing:**
```bash
make install
make pipeline
```

**Run just one component:**
```bash
PYTHONPATH=. python3 pipelines/training_flow.py
```

---

## Aliases (Optional)

Add to your `.bashrc` or `.zshrc`:
```bash
alias pipeline="cd /path/to/project && make pipeline"
alias train="cd /path/to/project && make train"
alias api="cd /path/to/project && make api"
```

Then use:
```bash
pipeline  # Run full pipeline
train     # Run training only
api       # Start API
```
