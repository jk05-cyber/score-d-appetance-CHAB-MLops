import os
from pathlib import Path

# base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "src" / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
SCORED_DIR = DATA_DIR / "scored"

MLRUNS_DIR = BASE_DIR / "mlruns"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"

# raw data files
RC_FILE = RAW_DIR / "RC.csv"
PC_FILE = RAW_DIR / "PC.csv"
MOUVEMENT_FILE = RAW_DIR / "MOUVEMENT.csv"

# modeling configuration
ID_COL = "ID_CLIENT"
TARGET_COLUMN = "chab_target"

RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.1

# feature lists (populated later)
NUMERIC_FEATURES = []
CATEGORICAL_FEATURES = []

# validation thresholds
REQUIRED_COLUMNS = {
    "RC": ["ID_CLIENT", "AGE", "DATE_ENTREE_BANQUE"],
    "PC": ["ID_CLIENT", "TYPE_PRODUIT", "DATE_SOUSCRIPTION"],
    "MOUVEMENT": ["ID_CLIENT", "MONTANT", "DATE_OPERATION"]
}

MISSING_VALUE_THRESHOLD = 0.2
DUPLICATE_THRESHOLD = 0.0

# API parameters
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# monitoring parameters
DRIFT_THRESHOLD = 0.1
