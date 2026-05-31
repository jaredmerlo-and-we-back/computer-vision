import os
import shutil
from datetime import datetime

import numpy as np
import torch
import open_clip
from PIL import Image
from flask import Flask, request, render_template, send_from_directory
from pymilvus import MilvusClient

# ----------------------------
# Config (matches Colab notebook defaults)
# ----------------------------
DRIVE_ROOT = os.environ.get("DRIVE_ROOT", "/content/drive/MyDrive/YogaPoseSearch")
DB_PATH = os.environ.get("DB_PATH", os.path.join(DRIVE_ROOT, "yoga_milvus.db"))
COLLECTION = os.environ.get("COLLECTION", "yoga_clip_embeddings")
TOP_N_DEFAULT = int(os.environ.get("TOP_N_DEFAULT", "5"))

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(APP_ROOT, "static", "uploads")
RESULTS_DIR = os.path.join(APP_ROOT, "static", "results")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Limit upload size (default 10MB)
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_CONTENT_LENGTH", str(10 * 1024 * 1024)))

# ----------------------------
# Model (CLIP)
# ----------------------------
_device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, _, clip_preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="openai")
clip_model = clip_model.to(_device).eval()


def _l2_normalize(x: np.ndarray) -> np.ndarray:
    return x / (np.linalg.norm(x) + 1e-10)


def get_image_embedding(image_path: str) -> np.ndarray:
    img = Image.open(image_path).convert("RGB")
    img_t = clip_preprocess(img).unsqueeze(0).to(_device)
    with torch.no_grad():
        emb = clip_model.encode_image(img_t).squeeze().cpu().numpy()
    return _l2_normalize(emb).astype(np.float32)


def milvus_search_by_image(image_path: str, top_n: int) -> list[dict]:
    query_vec = get_image_embedding(image_path)
    c = MilvusClient(DB_PATH)
    try:
        res = c.search(
            collection_name=COLLECTION,
            data=[query_vec],
            limit=top_n,
            output_fields=["label", "image_path"],
            search_params={"metric_type": "COSINE"},
        )
    finally:
        c.close()

    hits = []
    for h in res[0]:
        hits.append(
            {
                "score": round(float(h["distance"]), 4),
                "label": h["entity"].get("label"),
                "image_path": h["entity"].get("image_path"),
            }
        )
    return hits


def _safe_copy_result_image(src_path: str) -> str | None:
    """Copy a dataset image into static/results so the browser can display it."""
    if not src_path or not os.path.exists(src_path):
        return None

    # Use timestamp + basename to avoid collisions
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    base = os.path.basename(src_path)
    out_name = f"{ts}_{base}"
    out_path = os.path.join(RESULTS_DIR, out_name)

    try:
        shutil.copy(src_path, out_path)
        return out_name
    except Exception:
        return None


@app.get("/")
def index():
    return render_template(
        "index.html",
        top_n_default=TOP_N_DEFAULT,
        db_path=DB_PATH,
        collection=COLLECTION,
        device=_device,
    )


@app.post("/search")
def search():
    if "image" not in request.files:
        return render_template("index.html", error="No file field named 'image' found.", top_n_default=TOP_N_DEFAULT)

    f = request.files["image"]
    if not f or not f.filename:
        return render_template("index.html", error="No image selected.", top_n_default=TOP_N_DEFAULT)

    # Parse top_n
    try:
        top_n = int(request.form.get("top_n", str(TOP_N_DEFAULT)))
        top_n = max(1, min(top_n, 50))
    except Exception:
        top_n = TOP_N_DEFAULT

    # Save upload
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    upload_name = f"{ts}_{os.path.basename(f.filename)}"
    upload_path = os.path.join(UPLOAD_DIR, upload_name)
    f.save(upload_path)

    # Search
    try:
        hits = milvus_search_by_image(upload_path, top_n=top_n)
    except Exception as e:
        return render_template(
            "index.html",
            error=f"Search failed: {type(e).__name__}: {e}",
            top_n_default=TOP_N_DEFAULT,
            db_path=DB_PATH,
            collection=COLLECTION,
            device=_device,
        )

    # Copy hit images into /static/results for display
    rendered_hits = []
    for h in hits:
        copied = _safe_copy_result_image(h.get("image_path"))
        rendered_hits.append(
            {
                **h,
                "result_static_name": copied,
            }
        )

    return render_template(
        "results.html",
        upload_name=upload_name,
        top_n=top_n,
        hits=rendered_hits,
    )


@app.get("/uploads/<path:filename>")
def uploaded_file(filename: str):
    return send_from_directory(UPLOAD_DIR, filename)


@app.get("/results/<path:filename>")
def result_file(filename: str):
    return send_from_directory(RESULTS_DIR, filename)


if __name__ == "__main__":
    # For Colab/ngrok: run on 0.0.0.0
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
