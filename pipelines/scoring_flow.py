"""Pipeline for batch scoring of new data."""
from src.data.load_data import load_rc, load_pc, load_mouvement
from src.features.feature_pipeline import create_feature_set, prepare_for_model
from src.models.predict import predict
from src.config import settings


def run(rc_path=None, pc_path=None, mv_path=None, output_path=None):
    rc = load_rc(rc_path)
    pc = load_pc(pc_path)
    mv = load_mouvement(mv_path)
    feats = create_feature_set(rc, pc, mv)
    X, _ = prepare_for_model(feats)
    preds = predict(X)
    preds["ID_CLIENT"] = feats["ID_CLIENT"].values
    out_path = output_path or (settings.SCORED_DIR / "batch_scores.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    preds.to_csv(out_path, index=False)
    return preds


if __name__ == "__main__":
    run()
