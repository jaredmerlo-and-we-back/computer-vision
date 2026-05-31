# YogaPose Vector Search Web App (Flask + Milvus + CLIP)

This app is designed to run alongside the `YogaPose_VectorSearch_Colab.ipynb` pipeline.

## What it does
- Lets you upload a yoga image from your computer
- Lets you set `N` (top-k) nearest neighbors
- Runs CLIP image embedding
- Searches Milvus (`milvus-lite` DB file) for nearest images
- Displays results in a browser

## Expected setup
You should have already built the Milvus database in Colab so that:
- `DB_PATH` exists on Drive
- `COLLECTION` exists and contains vectors with `label` and `image_path`

## Run locally
```bash
cd flask_app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Run in Colab
In a Colab cell:
```python
!pip install -r flask_app/requirements.txt

# If your code is running from repo root:
%cd flask_app

# Start Flask in background
import threading, subprocess
threading.Thread(target=lambda: subprocess.call(["python", "app.py"]), daemon=True).start()

# Expose port 5000
from pyngrok import ngrok
public_url = ngrok.connect(5000)
print(public_url)
```

## Configuration
These environment variables override defaults:
- `DRIVE_ROOT` (default: `/content/drive/MyDrive/YogaPoseSearch`)
- `DB_PATH` (default: `$DRIVE_ROOT/yoga_milvus.db`)
- `COLLECTION` (default: `yoga_clip_embeddings`)
- `TOP_N_DEFAULT` (default: `5`)
