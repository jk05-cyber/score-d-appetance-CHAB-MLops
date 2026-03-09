# Credit Habitat Appetence Score (CHAB) - MLOps Project

Ce dépôt contient un projet Python structuré pour construire un modèle de scoring
d’appétence au crédit habitat. L’architecture est pensée pour être production-ready,
modulaire, testable et reproductible.

## 🧩 Architecture

```
credit_habitat_mlops/
│
├── data/               # stockage des jeux de données
├── notebooks/          # analyses exploratoires et debugging
├── src/                # code principal
├── pipelines/          # scripts d’orchestration
├── tests/              # tests unitaires
├── mlruns/             # tracking MLflow
├── models/             # modèles sauvegardés
├── reports/            # rapports de monitoring
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

## 📊 Données

Trois tables sources :

* `RC.csv` : référentiel clients (signalétique, profil)
* `PC.csv` : produits/comptes détenus par les clients
* `MOUVEMENT.csv` : historique transactionnel

Les données brutes sont poussées dans `data/raw/`. Le pipeline `src/data/build_dataset.py`
génère `data/processed/dataset.csv` utilisé pour l’entraînement.

## 🎯 Hypothèse de cible

La cible `chab_target` est construite par une hypothèse métier simple :
un client est considéré **positif** s’il a souscrit un produit de type `habitat_loan`
dans l’année écoulée. Cette approximation permet de simuler un signal d’intention
d’achat immobilier.

*Limites* : règle artificielle, dépend du type de produit présent dans les données.
Dans un contexte réel, il faudrait intégrer des règles commerciales et valider
les définitions avec les experts métier.

## � Usage

### Prerequisites
- Python 3.11+
- Install dependencies: `pip install -r requirements.txt`

### Running the Pipelines

1. **Training Pipeline**:
   ```bash
   python pipelines/training_flow.py
   ```
   This builds the dataset, engineers features, trains models (Logistic Regression and Random Forest), and logs results to MLflow.

2. **Scoring Pipeline**:
   ```bash
   python pipelines/scoring_flow.py
   ```
   This loads the trained model and scores all clients in the data, saving predictions to `src/data/scored/batch_scores.csv`.

### Running the API

Start the FastAPI service:
```bash
uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

### Running Tests

```bash
pytest tests/
```

### Containerization

Build and run with Docker Compose:
```bash
docker-compose up -d
```

This starts the API and MLflow server.

## 📈 Monitoring

Run drift detection:
```bash
python -c "from src.monitoring.drift_report import generate_report; print(generate_report('src/data/processed/dataset.csv', 'src/data/scored/batch_scores.csv'))"
```

## 🧪 Model Improvement

To improve the model:
- Experiment with additional features in `src/features/`
- Tune hyperparameters in `src/models/train.py`
- Try advanced models like XGBoost

## 📚 Documentation

- API docs available at `http://localhost:8000/docs` when running
- MLflow UI at `http://localhost:5000` for experiment tracking

* ingestion et validation des données (`src/data/`)
* feature engineering modulaire (`src/features/`)
* pipelines de training et scoring (`pipelines/`)
* modèles entrainés avec scikit-learn et trackés via MLflow
* API de scoring FastAPI (`src/api/app.py`)
* scripts de monitoring de drift (`src/monitoring/drift_report.py`)
* configuration centralisée, logging et gestion des chemins
* tests unitaires pour features, entraînement et API
* notebooks d’exploration et de debugging
* conteneurisation via Docker et docker-compose

## 🚀 Exécution

```bash
# installer
make install

# entraîner un modèle
make train

# scorer un lot de nouvelles données
make score

# lancer l’API localement
make api

# exécuter les tests
make test
```

Lancement via Docker :

```bash
docker-compose up --build
```

## 📦 Containers

Le service `api` expose l’application FastAPI sur le port `8000`.
Un service `mlflow` local est proposé sur le port `5000` pour le tracking.

## 🧪 Tests

Les tests utilisent `pytest` pour vérifier :

* la génération de features
* le bon déroulé du script d’entraînement
* le fonctionnement de l’API `/health` et `/predict`

## 📈 Monitoring

Le script `src/monitoring/drift_report.py` compare les distributions
features/score entre jeu d’entraînement et données scorées, et produit un rapport
CSV dans `reports/`.

## 🔧 Pistes d’amélioration

* enrichir les features (textes, géo, comportements)
* ajouter des tests d’intégration
* gérer la configuration via YAML et profiles
* intégrer un orchestrateur (Airflow, MLflow pipelines)
* déployer sur un cloud, monitorer en temps réel

---

Ce projet sert de modèle de référence pour un cycle MLops bancaire autour du scoring
crédit habitat.
