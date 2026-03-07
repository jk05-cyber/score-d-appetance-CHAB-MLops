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

## 🛠️ Fonctionnalités implémentées

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
