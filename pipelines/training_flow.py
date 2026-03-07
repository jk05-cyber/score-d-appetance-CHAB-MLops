"""Simple orchestration for training pipeline."""
from src.data.build_dataset import build_dataset
from src.models.train import train_models


def run():
    # create processed data
    build_dataset()
    # train models and log metrics
    results = train_models()
    print("Training complete. Best model:", results.get("best"))


if __name__ == "__main__":
    run()
