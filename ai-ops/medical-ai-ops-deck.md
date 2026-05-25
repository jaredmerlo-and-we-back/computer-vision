---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
html: true
style: |
  :root {
    --google-blue: #1a73e8;
    --google-light-blue: #e8f0fe;
    --google-border: #4285F4;
    --text-dark: #202124;
    --text-mid: #5f6368;
  }
  section {
    font-family: Arial, sans-serif;
    color: var(--text-dark);
    padding: 40px 50px;
  }
  h1 { color: var(--google-blue); font-size: 2em; }
  h2 { color: var(--google-blue); font-size: 1.4em; border-bottom: 2px solid var(--google-blue); padding-bottom: 6px; }
  h3 { color: var(--text-mid); font-size: 1em; }
  .icon-placeholder {
    width: 48px;
    height: 48px;
    background-color: var(--google-light-blue);
    border: 2px dashed var(--google-border);
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 7px;
    text-align: center;
    color: var(--google-border);
    font-weight: bold;
    line-height: 1.1;
    padding: 2px;
    box-sizing: border-box;
  }
  .node {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    width: 84px;
    font-size: 10px;
    text-align: center;
    vertical-align: top;
  }
  .flow-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 6px;
    margin: 14px 0;
    flex-wrap: wrap;
  }
  .arrow {
    font-size: 20px;
    color: #5f6368;
    line-height: 48px;
  }
  .divider-slide {
    background: var(--google-blue) !important;
  }
  .divider-slide h1 {
    color: white !important;
    border: none;
  }
  .divider-slide p {
    color: #cce0ff;
  }
  table { font-size: 12px; width: 100%; border-collapse: collapse; }
  th { background: #e8f0fe; color: #1a73e8; padding: 6px 8px; }
  td { padding: 5px 8px; border-bottom: 1px solid #e0e0e0; }
  blockquote {
    border-left: 4px solid var(--google-blue);
    padding-left: 12px;
    color: var(--text-mid);
    font-style: italic;
    margin: 10px 0;
  }
---

# Medical AI Ops
## GCP-Based DevOps Lifecycle for AI Workflows
### Cancer Classification & Skin Condition Segmentation

---

## Agenda

1. 🧬 **Medical AI Application Overview**
2. 🧪 **Initial Model Development**
3. 🔁 **Model Improvement**
   - Incremental training data addition
   - Clinician feedback & labeling loop
4. 📊 **Model Monitoring**
   - Drift & performance
   - Access & security
5. 🚀 **Productionalization**
6. 🖥️ **End User Interaction & Feedback**
   - UI implementation & cloud monitoring
   - Clinician feedback loop
7. 🗺️ **Full AI Ops Lifecycle**

---

## Medical AI Application Overview

Two core AI capabilities deployed on **Google Cloud Platform**:

| Capability | Task Type | Input Data | Clinical Value |
|---|---|---|---|
| 🔬 **Cancer Classification** | Multi-class classification | Pathology / radiology images | Early detection & triage support |
| 🩺 **Skin Condition Segmentation** | Semantic segmentation | Dermatology images | Lesion boundary mapping |

**Primary End Users:** Physicians & Nurses

**Compliance Scope:** HIPAA · Medical imaging data · Audit logging

---

<!-- _class: divider-slide -->

# 1. Initial Model Development

Building baseline models from curated medical imaging datasets

---

## Initial Model Development — Architecture

<div class="flow-row">
  <div class="node">
    <div class="icon-placeholder">Cloud Healthcare API</div>
    <span>Cloud Healthcare API</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Storage</div>
    <span>Cloud Storage (GCS)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Workbench</div>
    <span>Vertex AI Workbench</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Training</div>
    <span>Vertex AI Training</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Model Registry</div>
    <span>Model Registry</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Artifact Registry</div>
    <span>Artifact Registry</span>
  </div>
</div>

**Key Steps:**
- Ingest DICOM / medical images via **Cloud Healthcare API**
- Store raw datasets & model artifacts in **Cloud Storage (GCS)**
- Experiment and prototype in **Vertex AI Workbench** notebooks
- Run and track training jobs via **Vertex AI Training**
- Version and register model checkpoints in **Vertex AI Model Registry**
- Store container images in **Artifact Registry** for reproducibility

---

<!-- _class: divider-slide -->

# 2. Model Improvement

Continuous learning through new data and clinician-driven feedback

---

## Model Improvement — Incremental Training Data

<div class="flow-row">
  <div class="node">
    <div class="icon-placeholder">Cloud Healthcare API</div>
    <span>New Data Ingestion</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Pub/Sub</div>
    <span>Cloud Pub/Sub (trigger)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Pipelines</div>
    <span>Vertex AI Pipelines</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Feature Store</div>
    <span>Feature Store</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Training</div>
    <span>Incremental Training</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Model Registry</div>
    <span>New Model Version</span>
  </div>
</div>

- New medical images arriving via **Cloud Healthcare API** publish events to **Pub/Sub**
- **Pub/Sub** triggers an automated **Vertex AI Pipeline** run
- Pipeline orchestrates: data validation → preprocessing → training → evaluation
- **Feature Store** manages reusable feature sets across training runs
- Passing models are promoted as new versions in **Model Registry**

---

## Model Improvement — Clinician Feedback & Labeling

<div class="flow-row">
  <div class="node">
    <div class="icon-placeholder">Cloud Run UI</div>
    <span>Clinician UI</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Firestore</div>
    <span>Firestore (Feedback Store)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Pub/Sub</div>
    <span>Cloud Pub/Sub</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Data Labeling</div>
    <span>Vertex AI Data Labeling</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Pipelines</div>
    <span>Retraining Pipeline</span>
  </div>
</div>

- Physicians and nurses flag incorrect predictions or annotate new cases via the **UI**
- Feedback is persisted in **Firestore** and streamed via **Cloud Pub/Sub**
- **Vertex AI Data Labeling** facilitates managed labeling workflows for flagged cases
- Labeled cases feed directly into the **retraining pipeline** as new ground truth

> 💡 This implements a **human-in-the-loop** active learning cycle, closing the gap between clinical expertise and model accuracy.

---

<!-- _class: divider-slide -->

# 3. Model Monitoring

Continuous observability over model performance, drift, and access

---

## Model Monitoring — Drift & Performance

<div class="flow-row">
  <div class="node">
    <div class="icon-placeholder">Vertex AI Endpoints</div>
    <span>Vertex AI Endpoints (Live Traffic)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Model Monitoring</div>
    <span>Model Monitoring</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Monitoring</div>
    <span>Cloud Monitoring</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Alerting</div>
    <span>Cloud Alerting</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Pipelines</div>
    <span>Auto Retrain Trigger</span>
  </div>
</div>

| Monitoring Type | GCP Tool | Signal |
|---|---|---|
| **Prediction drift** | Vertex AI Model Monitoring | Input / output distribution shift |
| **Training-serving skew** | Vertex AI Model Monitoring | Feature distribution delta vs. baseline |
| **Latency & throughput** | Cloud Monitoring | p50 / p95 / p99 endpoint latency |
| **Error rates** | Cloud Monitoring | 4xx / 5xx on inference endpoints |
| **Automated alerting** | Cloud Alerting | Threshold-based notifications to on-call |

---

## Model Monitoring — Access & Security

<div class="flow-row">
  <div class="node">
    <div class="icon-placeholder">Cloud IAM</div>
    <span>Cloud IAM</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Identity-Aware Proxy</div>
    <span>Identity-Aware Proxy (IAP)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Endpoints</div>
    <span>Vertex AI Endpoints</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Logging</div>
    <span>Cloud Audit Logs</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Monitoring</div>
    <span>Anomaly Alerts</span>
  </div>
</div>

**Key Considerations:**
- 🔐 **Cloud IAM** — Role-based access control for model endpoints (clinicians, admins, service accounts)
- 🛡️ **Identity-Aware Proxy (IAP)** — Zero-trust authentication gate for all UI and API access
- 📋 **Cloud Audit Logs** — Immutable trail: who accessed which model, when, and from where
- 🏥 **HIPAA Alignment** — Logging, encryption at rest/in transit, and access controls support compliance obligations
- 🔔 **Anomaly Alerting** — Notify on unauthorized or unusual access patterns

---

<!-- _class: divider-slide -->

# 4. Productionalization

Promoting validated models through a governed CI/CD pipeline into production

---

## Productionalization — Architecture

<div class="flow-row">
  <div class="node">
    <div class="icon-placeholder">Vertex AI Pipelines</div>
    <span>Evaluation Gate (Pipelines)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Build</div>
    <span>Cloud Build (CI/CD)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Artifact Registry</div>
    <span>Artifact Registry</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Endpoints</div>
    <span>Vertex AI Endpoints</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Load Balancing</div>
    <span>Cloud Load Balancing</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Run</div>
    <span>Cloud Run (API Layer)</span>
  </div>
</div>

**Deployment Pipeline Steps:**
1. Model passes automated evaluation gates in **Vertex AI Pipelines** (accuracy, latency thresholds)
2. **Cloud Build** packages container image and pushes to **Artifact Registry**
3. Model deployed to **Vertex AI Endpoint** using blue/green or canary strategy
4. **Cloud Load Balancing** routes and splits traffic across model versions
5. **Cloud Run** serves as the managed API layer between the UI and model endpoints
6. Automated rollback triggered on performance degradation alerts

---

<!-- _class: divider-slide -->

# 5. End User Interaction & Feedback

Clinician-facing UI, cloud logging, and feedback-driven improvement

---

## End User UI — Architecture

<div class="flow-row">
  <div class="node">
    <div class="icon-placeholder">Identity-Aware Proxy</div>
    <span>IAP (Auth Gate)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Run</div>
    <span>Cloud Run (UI Host)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Run</div>
    <span>Cloud Run (Inference API)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Endpoints</div>
    <span>Vertex AI Endpoints</span>
  </div>
</div>

<div class="flow-row">
  <div class="node">
    <div class="icon-placeholder">Cloud Logging</div>
    <span>Cloud Logging (UI Events)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Monitoring</div>
    <span>Cloud Monitoring (Dashboards)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Alerting</div>
    <span>Cloud Alerting</span>
  </div>
</div>

- **IAP** ensures only authenticated clinicians can access the application
- **Cloud Run** hosts the frontend and inference API — fully managed, auto-scaling
- All UI events (clicks, queries, errors) captured in **Cloud Logging** for audit and UX analysis
- **Cloud Monitoring** dashboards track UI errors, session latency, and usage volume

---

## Clinician Feedback Loop

<div class="flow-row">
  <div class="node">
    <div class="icon-placeholder">Cloud Run UI</div>
    <span>Feedback Form (UI)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Firestore</div>
    <span>Firestore (Response Store)</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Pub/Sub</div>
    <span>Cloud Pub/Sub</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Data Labeling</div>
    <span>Data Labeling</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Pipelines</div>
    <span>Retraining Pipeline</span>
  </div>
</div>

**Feedback Categories Captured:**

| Category | Description |
|---|---|
| ✅ **Prediction Correctness** | Was the classification / segmentation accurate? |
| 🖊️ **Label Corrections** | Clinician re-annotates incorrect model outputs |
| 💬 **UX Feedback** | Free-text comments on interface usability |
| ⭐ **Case Flagging** | High-value or edge-case images flagged for priority labeling |

---

## Full AI Ops Lifecycle

<div class="flow-row">
  <div class="node">
    <div class="icon-placeholder">Cloud Healthcare API</div>
    <span>Data Ingestion</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Workbench</div>
    <span>Experimentation</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Pipelines</div>
    <span>Training Pipeline</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Model Registry</div>
    <span>Model Registry</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Build</div>
    <span>CI/CD</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Endpoints</div>
    <span>Production Endpoints</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Cloud Run UI</div>
    <span>Clinician UI</span>
  </div>
</div>

**Continuous Improvement Loop:**

<div class="flow-row">
  <div class="node">
    <div class="icon-placeholder">Vertex AI Model Monitoring</div>
    <span>Drift Monitoring</span>
  </div>
  <div class="arrow">+</div>
  <div class="node">
    <div class="icon-placeholder">Firestore</div>
    <span>Feedback Store</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Data Labeling</div>
    <span>Labeling</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Pipelines</div>
    <span>Retraining</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <div class="icon-placeholder">Vertex AI Model Registry</div>
    <span>New Model Version</span>
  </div>
</div>

---

## Summary — Key AI Ops Pillars on GCP

| Pillar | GCP Services |
|---|---|
| 🧪 **Development** | Cloud Healthcare API · Cloud Storage · Vertex AI Workbench · Vertex AI Training |
| 🔁 **Improvement** | Cloud Pub/Sub · Vertex AI Pipelines · Data Labeling · Feature Store |
| 📊 **Monitoring** | Vertex AI Model Monitoring · Cloud Monitoring · Cloud Logging · Cloud IAM |
| 🚀 **Production** | Cloud Build · Artifact Registry · Vertex AI Endpoints · Cloud Load Balancing |
| 🖥️ **User & Feedback** | Cloud Run · IAP · Firestore · Cloud Pub/Sub |

> **Icon placeholders** — dashed blue boxes (48×48 px) mark locations for official GCP service icons.
> Download icons from: [https://cloud.google.com/icons](https://cloud.google.com/icons)
