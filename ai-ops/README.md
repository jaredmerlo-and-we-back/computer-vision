# Medical AI Ops Deck

This directory contains the AI Ops presentation deck for the GCP-based Medical AI application covering **Cancer Classification** and **Skin Condition Segmentation**.

## Files

| File | Description |
|---|---|
| `medical-ai-ops-deck.md` | Marp Markdown slide deck with GCP architecture diagrams |

---

## How to Export to PPTX or Google Slides

### Option A — Export to `.pptx` directly (Marp CLI)

1. Install Marp CLI:
   ```bash
   npm install -g @marp-team/marp-cli
   ```

2. Export to PowerPoint:
   ```bash
   marp medical-ai-ops-deck.md --pptx --html --output medical-ai-ops.pptx
   ```

3. Open `medical-ai-ops.pptx` in PowerPoint or upload to Google Drive → open with Google Slides.

---

### Option B — Export to PDF, then import to Google Slides

1. Export to PDF:
   ```bash
   marp medical-ai-ops-deck.md --pdf --html --output medical-ai-ops.pdf
   ```

2. Go to [Google Slides](https://slides.google.com) → **File → Import slides** → upload the PDF.

---

### Option C — Preview in VS Code (no CLI needed)

1. Install the [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) extension.
2. Open `medical-ai-ops-deck.md`.
3. Click the **Marp preview** button (top right) to render slides.
4. Use **Export slide deck** from the Marp VS Code menu to export as PPTX or PDF.

---

## Replacing Icon Placeholders

All architecture diagrams contain **48×48 px placeholder boxes** (dashed blue borders) labelled with the GCP service name.

To replace them with official GCP icons:

1. Download the official GCP icon pack from: **https://cloud.google.com/icons**
2. After exporting to PPTX, replace each placeholder box with the corresponding icon image.
3. Icons are organized by product family in the GCP icon pack ZIP file.

### GCP Icon Reference

| Service | Icon File Name (in GCP pack) |
|---|---|
| Cloud Healthcare API | `cloud_healthcare_api` |
| Cloud Storage | `cloud_storage` |
| Vertex AI Workbench | `vertex_ai` |
| Vertex AI Training | `vertex_ai` |
| Vertex AI Pipelines | `vertex_ai_pipelines` |
| Vertex AI Model Registry | `vertex_ai` |
| Vertex AI Endpoints | `vertex_ai` |
| Vertex AI Model Monitoring | `vertex_ai` |
| Vertex AI Data Labeling | `vertex_ai` |
| Vertex AI Feature Store | `vertex_ai` |
| Cloud Build | `cloud_build` |
| Artifact Registry | `artifact_registry` |
| Cloud Run | `cloud_run` |
| Cloud Load Balancing | `cloud_load_balancing` |
| Cloud Pub/Sub | `cloud_pubsub` |
| Cloud Monitoring | `cloud_monitoring` |
| Cloud Logging | `cloud_logging` |
| Cloud IAM | `cloud_iam` |
| Identity-Aware Proxy (IAP) | `identity_aware_proxy` |
| Firestore | `firestore` |
| Cloud Composer | `cloud_composer` |

---

## Slide Structure

| Slide | Title |
|---|---|
| 1 | Title — Medical AI Ops |
| 2 | Agenda |
| 3 | Medical AI Application Overview |
| 4 | Section Divider — Initial Model Development |
| 5 | Initial Model Development — Architecture |
| 6 | Section Divider — Model Improvement |
| 7 | Model Improvement — Incremental Training Data |
| 8 | Model Improvement — Clinician Feedback & Labeling |
| 9 | Section Divider — Model Monitoring |
| 10 | Model Monitoring — Drift & Performance |
| 11 | Model Monitoring — Access & Security |
| 12 | Section Divider — Productionalization |
| 13 | Productionalization — Architecture |
| 14 | Section Divider — End User Interaction & Feedback |
| 15 | End User UI — Architecture |
| 16 | Clinician Feedback Loop |
| 17 | Full AI Ops Lifecycle |
| 18 | Summary — Key AI Ops Pillars |
