"""Model registration script."""
import mlflow


def register_model(run_id: str, name: str):
    """Register an MLflow run artifact under the given name."""
    client = mlflow.tracking.MlflowClient()
    mv = client.get_run(run_id).info
    # assume model artifact at 'model'
    model_uri = f"runs:/{run_id}/model"
    registered = client.create_registered_model(name)
    client.create_model_version(name, model_uri, run_id)
    return registered
