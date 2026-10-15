# DevOps FA2 — CI/CD, Container Orchestration and Observability

[![FA2 CI/CD Pipeline](https://github.com/ShrutiDhupad/DevOps-FA1/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/ShrutiDhupad/DevOps-FA1/actions/workflows/ci-cd.yml)

## 1. Project Overview

This project extends the **FA1 Infrastructure as Code & Multi-Environment Container Deployment** project into a complete, enterprise-grade **FA2 DevOps Assessment Platform**. It demonstrates end-to-end continuous integration, automated testing, container image packaging and publishing to GitHub Container Registry (GHCR), declarative container orchestration with Kubernetes on Minikube, and full-stack observability with Prometheus and Grafana.

---

## 2. Objectives

- Automate the build, test, and release lifecycle using GitHub Actions.
- Ensure regression prevention through automated unit and integration tests.
- Package frontend and backend applications into minimal, secure, and reproducible Docker images.
- Publish immutable container images tagged with Git commit SHAs to GitHub Container Registry (GHCR).
- Orchestrate multi-container deployments across a dedicated Kubernetes namespace (`fa2-devops`).
- Implement zero-downtime rolling updates, resource boundaries, and health probes (readiness/liveness).
- Demonstrate dynamic scaling and rollback capabilities.
- Instrument the backend API using the official Prometheus Python client library.
- Scrape application and business metrics into Prometheus.
- Automatically provision interactive Grafana dashboards visualizing real-time HTTP metrics, request latencies, and service availability.

---

## 3. Technology Stack

- **Version Control & CI/CD:** Git, GitHub, GitHub Actions, GitHub Container Registry (GHCR)
- **Containerization & Local Dev:** Docker, Docker Compose, Multi-stage Dockerfiles
- **Container Orchestration:** Kubernetes, Minikube, Kustomize, `kubectl`
- **Backend API:** Python 3.12, Flask 3.1, `prometheus-client`, `pytest`
- **Frontend Reverse Proxy & UI:** Nginx Alpine, Vanilla HTML5 / Modern CSS Glassmorphism / JavaScript
- **Observability & Metrics:** Prometheus 2.54, Grafana 11.2, PromQL

---

## 4. Architecture Diagram

```text
 Developer Workstation
         │
         │  git push origin main
         ▼
 ┌──────────────────────────────────────────────────────────────┐
 │                GitHub Actions CI/CD Pipeline                 │
 │                                                              │
 │   1. Checkout Source Code                                    │
 │   2. Setup Python 3.12 & Dependencies                        │
 │   3. Run 15 Automated Tests (pytest)                         │
 │   4. Validate Docker Compose & Kustomize Manifests           │
 │   5. Build Docker Images (frontend & backend)                │
 │   6. Tag Images with Commit SHA & Push to GHCR               │
 └──────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │             GitHub Container Registry (GHCR)                 │
 │   • ghcr.io/shrutidhupad/fa2-backend:<sha>                   │
 │   • ghcr.io/shrutidhupad/fa2-frontend:<sha>                  │
 └──────────────────────────────┬───────────────────────────────┘
                                │
                                │  kubectl apply -k k8s/
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │               Kubernetes Cluster (fa2-devops)                │
 │                                                              │
 │   ┌────────────────────────┐    ┌────────────────────────┐   │
 │   │   Frontend Service     │    │    Backend Service     │   │
 │   │   (NodePort: 30080)    │    │   (ClusterIP: 5000)    │   │
 │   └───────────┬────────────┘    └───────────▲────────────┘   │
 │               │                             │                │
 │               ▼                             │                │
 │   ┌────────────────────────┐    ┌───────────┴────────────┐   │
 │   │  Frontend Deployment   │───►│   Backend Deployment   │   │
 │   │  (Nginx Reverse Proxy) │HTTP│  (Flask API + Metrics) │   │
 │   └────────────────────────┘    └───────────┬────────────┘   │
 │                                             │                │
 │                                             │ scrape :5000   │
 │   ┌────────────────────────┐    ┌───────────▼────────────┐   │
 │   │   Grafana Dashboard    │◄───│  Prometheus Collector  │   │
 │   │      (Port: 3000)      │    │      (Port: 9090)      │   │
 │   └────────────────────────┘    └────────────────────────┘   │
 └──────────────────────────────────────────────────────────────┘
```

---

## 5. Existing FA1 Functionality (Preserved)

- Multi-environment Infrastructure as Code using Terraform (`terraform/` directory with `qa`, `uat`, `prod` configurations).
- Python Flask backend with existing endpoints:
  - `GET /` — Backend status and environment.
  - `GET /api/hello` — Greeting message from backend.
- Nginx frontend container acting as a web host and reverse proxy for backend API calls.
- Full backwards-compatible UI hooks (`callBackend()`, `#result` element).

---

## 6. New FA2 Functionality Added

- **Health Probes:** Added `/health` and `/api/health` endpoints for Kubernetes readiness and liveness checks.
- **Business Logic & Validation:** Added `GET /api/items` and `POST /api/items` with payload validation (HTTP 400 on error, HTTP 201 on success).
- **Automated Test Suite:** Created 15 automated unit tests in `tests/test_backend.py` and `tests/test_frontend.py`.
- **Prometheus Instrumentation:** Custom HTTP request counters (`http_requests_total`), request duration histograms (`http_request_duration_seconds`), and business counters (`items_created_total`).
- **Modern UI:** Responsive, glassmorphism dashboard with real-time health indicator, item management forms, and live metric preview.
- **Docker Compose:** Added root `docker-compose.yml` for unified local running and `monitoring/docker-compose.monitoring.yml` for local Prometheus/Grafana stacks.
- **GitHub Actions CI/CD:** `.github/workflows/ci-cd.yml` supporting push/PR triggers, automated tests, GHCR builds, and Kustomize dry-run validations.
- **Kubernetes Architecture:** Declarative manifests under `k8s/` implementing namespace, deployments, ClusterIP, NodePort, rolling update strategies, and resource constraints.
- **Grafana Provisioning:** Automated datasource and dashboard provisioning under `monitoring/grafana/` featuring 5 live panels.

---

## 7. Directory Structure

```text
DevOps-FA1/
├── .github/
│   └── workflows/
│       └── ci-cd.yml                 # GitHub Actions 3-stage CI/CD pipeline
├── docker/
│   ├── backend/
│   │   ├── Dockerfile                # Hardened backend Dockerfile with non-root user
│   │   ├── .dockerignore
│   │   ├── app.py                    # Flask API + Prometheus instrumentation
│   │   └── requirements.txt          # Python dependencies (Flask, prometheus-client, pytest)
│   └── frontend/
│       ├── Dockerfile                # Nginx Alpine Dockerfile with health checks
│       ├── .dockerignore
│       ├── index.html                # Modern interactive frontend web dashboard
│       └── nginx.conf                # Nginx reverse proxy configuration
├── docs/
│   └── FINAL_SETUP_GUIDE.md          # Complete step-by-step manual setup & evaluation guide
├── k8s/
│   ├── 00-namespace.yaml             # Dedicated fa2-devops namespace
│   ├── 01-backend-deployment.yaml    # Backend deployment, probes, resources, annotations
│   ├── 02-backend-service.yaml       # Backend ClusterIP service on port 5000
│   ├── 03-frontend-deployment.yaml   # Frontend deployment, rolling update, health probes
│   ├── 04-frontend-service.yaml      # Frontend NodePort service on port 30080
│   └── kustomization.yaml            # Unified declarative Kustomize manifest
├── monitoring/
│   ├── prometheus.yml                # Prometheus scrape configuration targeting backend
│   ├── docker-compose.monitoring.yml # Local Docker Compose monitoring overlay
│   ├── grafana/
│   │   ├── dashboards/
│   │   │   └── fa2-dashboard.json    # Provisioned 5-panel Grafana dashboard JSON
│   │   └── provisioning/
│   │       ├── dashboards/
│   │       │   └── dashboards.yml    # Automatic dashboard provider configuration
│   │       └── datasources/
│   │           └── prometheus.yml    # Automatic Prometheus datasource configuration
│   └── k8s/
│       ├── 00-prometheus.yaml        # In-cluster Prometheus deployment & service
│       └── 01-grafana.yaml           # In-cluster Grafana deployment & service
├── tests/
│   ├── __init__.py
│   ├── test_backend.py               # 12 automated backend API & metric unit tests
│   └── test_frontend.py              # 3 automated frontend & reverse proxy tests
├── terraform/                        # Preserved FA1 Terraform infrastructure
├── .dockerignore                     # Root Docker build context ignore rules
├── .gitignore                        # Git ignore rules (venv, caches, logs)
├── docker-compose.yml                # Root multi-container local runtime
├── pytest.ini                        # Pytest configuration & options
└── README.md                         # Project documentation & rubric mapping
```

---

## 8. Prerequisites

- **Git:** 2.40+
- **Python:** 3.12+ (or Windows Python Launcher `py`)
- **Docker Desktop:** 24+ with Compose v2
- **Kubernetes CLI (`kubectl`):** 1.28+
- **Minikube:** 1.32+
- **Web Browser:** Chrome / Edge / Firefox

---

## 9. Local Application Setup & Automated Testing

### 1. Set Up Python Virtual Environment
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r docker/backend/requirements.txt
```

### 2. Execute Automated Test Suite
```powershell
pytest -v
```
*Result:* All 15 tests pass in < 1 second.

---

## 10. Docker Commands

Run the multi-container application locally:

```powershell
# 1. Build images
docker compose build

# 2. Start services in background
docker compose up -d

# 3. View running containers
docker compose ps

# 4. Inspect container logs
docker compose logs -f

# 5. Stop and remove containers
docker compose down
```

Access the local app at `http://localhost:8080`.

---

## 11. GitHub Actions CI/CD Workflow

The pipeline defined in `.github/workflows/ci-cd.yml` executes three stages:
1. **Stage 1 (test):** Checks out code, sets up Python 3.12, executes `pytest -v`, and verifies `docker compose config`.
2. **Stage 2 (build-and-push):** Triggers on push to `main`, logs in to GHCR via `GITHUB_TOKEN`, builds both Docker images, tags them with `${{ github.sha }}` and `latest`, and pushes to GHCR.
3. **Stage 3 (k8s-validate):** Runs `kubectl kustomize k8s/` to validate all Kubernetes manifests.

---

## 12. GitHub Container Registry (GHCR) Publishing

Images are published to:
- `ghcr.io/shrutidhupad/fa2-backend:<sha>` and `:latest`
- `ghcr.io/shrutidhupad/fa2-frontend:<sha>` and `:latest`

To pull and verify locally:
```powershell
docker pull ghcr.io/shrutidhupad/fa2-backend:latest
docker pull ghcr.io/shrutidhupad/fa2-frontend:latest
```

---

## 13. Kubernetes & Minikube Setup

Start Minikube:
```powershell
minikube start --driver=docker
```

Verify cluster connectivity:
```powershell
kubectl get nodes
```

---

## 14. Kubernetes Deployment Commands

Deploy all application resources in one command:
```powershell
kubectl apply -k k8s/
```

Verify deployment status:
```powershell
kubectl get all -n fa2-devops
```

Access frontend via Minikube:
```powershell
minikube service frontend-service -n fa2-devops
```
Or via port-forwarding:
```powershell
kubectl port-forward svc/frontend-service 8080:80 -n fa2-devops
```

---

## 15. Scaling and Rollout Demonstration

### Scaling Replicas
```powershell
# Scale frontend to 3 replicas
kubectl scale deployment/frontend-deployment --replicas=3 -n fa2-devops

# Verify running pods
kubectl get pods -l app=frontend -n fa2-devops
```

### Inspecting Rollout Status & History
```powershell
kubectl rollout status deployment/frontend-deployment -n fa2-devops
kubectl rollout history deployment/frontend-deployment -n fa2-devops
```

### Rolling Back a Deployment
```powershell
kubectl rollout undo deployment/frontend-deployment -n fa2-devops
```

---

## 16. Prometheus Configuration

Scrape config in `monitoring/prometheus.yml`:
```yaml
scrape_configs:
  - job_name: "fa2-backend"
    metrics_path: "/metrics"
    scrape_interval: 5s
    static_configs:
      - targets: ["backend:5000"]
```

Deploy in Kubernetes:
```powershell
kubectl apply -f monitoring/k8s/00-prometheus.yaml
kubectl port-forward svc/prometheus 9090:9090 -n fa2-devops
```

---

## 17. PromQL Examples

Execute these queries in Prometheus (`http://localhost:9090/graph`):
1. **Total HTTP Requests by Route and Status:**
   ```promql
   sum(http_requests_total) by (endpoint, status)
   ```
2. **Current Request Rate:**
   ```promql
   sum(rate(http_requests_total[1m]))
   ```
3. **95th Percentile Latency:**
   ```promql
   histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
   ```
4. **Application Availability:**
   ```promql
   up{job="fa2-backend"}
   ```
5. **Business Metric (Items Created):**
   ```promql
   items_created_total
   ```

---

## 18. Grafana Access and Dashboard Usage

1. Deploy Grafana in Kubernetes:
   ```powershell
   kubectl apply -f monitoring/k8s/01-grafana.yaml
   kubectl port-forward svc/grafana 3000:3000 -n fa2-devops
   ```
2. Open `http://localhost:3000` (Login: `admin` / `admin`).
3. Navigate to **Dashboards** > **DevOps Assessment** > **FA2 DevOps Observability Dashboard**.
4. The dashboard automatically displays:
   - Service Availability (UP/DOWN)
   - Current Request Rate (req/s gauge)
   - Total Items Created (Business Counter)
   - P95 Latency (seconds)
   - Total HTTP Requests timeseries chart
   - Duration histogram chart

---

## 19. Automated Testing Details

The test suite in `tests/` covers:
- Backend home endpoint (`test_home_endpoint`)
- FA1 greeting API (`test_hello_endpoint`)
- Kubernetes health endpoint (`test_health_endpoint`, `test_api_health_alias`)
- Item query and item creation (`test_get_items`, `test_create_item_success`)
- Input validation: missing name, whitespace name, non-JSON body (`test_create_item_missing_name_returns_400`, `test_create_item_empty_name_returns_400`, `test_create_item_non_json_returns_400`)
- Prometheus metrics exposition & request counters (`test_metrics_endpoint_availability`, `test_metrics_records_request`)
- Error handling: 404 responses (`test_not_found_endpoint`)
- Frontend HTML structure, backward compatibility IDs, and Nginx reverse proxy routes (`tests/test_frontend.py`)

---

## 20. Troubleshooting

- **Pod in `ErrImagePull` or `ImagePullBackOff`:** Ensure the package on GHCR is set to Public, or provide `imagePullSecrets`.
- **Backend returns 400 Bad Request:** Verify payload format is `{"name": "...", "description": "..."}` with `Content-Type: application/json`.
- **Prometheus target shows `DOWN`:** Check that the backend pod is running and service name `backend` resolves on port 5000.
- **Grafana shows `No data`:** Change time filter to "Last 15 minutes" and generate traffic via the frontend web UI.

---

## 21. Cleanup

### Kubernetes Cleanup
```powershell
kubectl delete -k k8s/
kubectl delete -f monitoring/k8s/
```

### Docker Cleanup
```powershell
docker compose down -v
```

---

## 22. Security Notes

- No secrets or personal access tokens are committed to the repository.
- Backend Docker container executes as an unprivileged user (`appuser`).
- Input validation prevents unbounded parameter injection into metrics.
- Kubernetes resources specify explicit CPU and memory boundaries to prevent resource exhaustion attacks.

---

## 23. Known Limitations

- In local Minikube environments, GHCR packages must either be public or use a configured secret.
- Standalone Minikube without an ingress controller uses NodePort and `port-forward` for browser access.

---

## 24. Final Practical Demonstration Checklist

See [docs/FINAL_SETUP_GUIDE.md](file:///C:/Users/Shruti/.gemini/antigravity-ide/scratch/DevOps-FA1/docs/FINAL_SETUP_GUIDE.md) for the exact step-by-step evaluation procedure.

---

## FA2 ASSESSMENT RUBRIC MAPPING (All 20 Marks)

| Mark | Rubric Assessment Criterion | Implementing File / Configuration | Exact Command or Screen to Demonstrate | Expected Result | Screenshot / Evidence to Capture | Local / CI Verification Status |
|:---:|---|---|---|---|---|:---:|
| **1** | Repository & source code in Git | Repository root, `.gitignore`, `.git` | `git status`, `git log -n 5 --oneline` | Clean working tree on `main`, clear commit history | Terminal showing commit history & origin remote | **Verified Locally** |
| **2** | Pipeline triggered through Git push | `.github/workflows/ci-cd.yml` | GitHub UI: **Actions** tab | Workflow runs automatically upon `git push origin main` | GitHub Actions workflow run header with push event | **Pending Git Push** |
| **3** | CI/CD tool configured | `.github/workflows/ci-cd.yml` | GitHub UI: `.github/workflows/ci-cd.yml` file view | Syntax-valid YAML workflow defining test, build, and deploy | Workflow YAML display in repository | **Verified Locally** |
| **4** | Pipeline performs checkout and build | `.github/workflows/ci-cd.yml` | GitHub UI: Job `test` step `Checkout Source Code` & `Install Dependencies` | Repository cloned and Python 3.12 dependencies installed | Step execution log showing successful checkout | **Pending Git Push** |
| **5** | Pipeline performs automated testing | `.github/workflows/ci-cd.yml` | GitHub UI: Job `test` step `Run Backend & Frontend Automated Tests` | Pytest executes all 15 tests and exits with code 0 | Step log showing `15 passed in 0.94s` | **Verified Locally (15 passed)** |
| **6** | Docker image built automatically | `.github/workflows/ci-cd.yml` | GitHub UI: Job `build-and-push` | Docker Buildx builds frontend and backend images | Step log showing successful image build layers | **Pending Git Push** |
| **7** | Pipeline completes end-to-end | `.github/workflows/ci-cd.yml` | GitHub UI: **Actions** run summary | All 3 jobs display green checkmarks | GitHub Actions run overview showing green checkmarks | **Pending Git Push** |
| **8** | Application builds successfully | `docker/backend/Dockerfile`, `docker/frontend/Dockerfile` | `docker compose config` | Compose parses services, builds, and networks cleanly | Terminal showing compose configuration output | **Verified Locally** |
| **9** | Meaningful automated test executed | `tests/test_backend.py`, `tests/test_frontend.py` | `.\.venv\Scripts\pytest.exe -v` | 15 tests pass covering health, API, validation, metrics | Terminal output showing 15 passed tests | **Verified Locally** |
| **10** | Pipeline fails when test fails | `.github/workflows/ci-cd.yml`, `tests/` | Push a temporary branch with failing test | Test step fails with exit code 1; build/push skipped | GitHub Actions red `X` on test step; downstream skipped | **Verified Locally / Documented** |
| **11** | Docker image/tag generated correctly | `.github/workflows/ci-cd.yml` | GitHub UI: **Packages** tab | Images tagged with Git commit SHA and `latest` | GHCR package detail showing commit SHA tag | **Pending Git Push** |
| **12** | Application successfully deployed | `k8s/`, `docker-compose.yml` | `kubectl get pods -n fa2-devops` / Browser `http://localhost:8080` | Frontend web page loads and communicates with backend | Browser showing UI with successful "Online" API badge | **Verified Locally (Compose)** |
| **13** | Kubernetes Deployment configuration | `k8s/01-backend-deployment.yaml`, `k8s/03-frontend-deployment.yaml` | `kubectl describe deployment backend-deployment -n fa2-devops` | Deployments show rolling update, probes, resource limits | Terminal output of `kubectl describe deployment` | **Verified Locally (Kustomize)** |
| **14** | Kubernetes Service configuration | `k8s/02-backend-service.yaml`, `k8s/04-frontend-service.yaml` | `kubectl get svc -n fa2-devops` | Backend ClusterIP (5000), Frontend NodePort (30080) | Terminal output of `kubectl get svc -n fa2-devops` | **Verified Locally (Kustomize)** |
| **15** | Application runs as Kubernetes pods | `k8s/` | `kubectl get pods -n fa2-devops` | Pods in `Running` state (`1/1 READY`) | Terminal output of running pods | **Ready on Minikube** |
| **16** | Scaling/rollout demonstrated | `k8s/03-frontend-deployment.yaml` | `kubectl scale deployment/frontend-deployment --replicas=3 -n fa2-devops` | Pod count increases from 2 to 3; rollout history inspected | Terminal showing scale command and 3 running pods | **Ready on Minikube** |
| **17** | Prometheus collecting metrics | `docker/backend/app.py`, `monitoring/prometheus.yml` | Browser `http://localhost:9090/targets` | Target `fa2-backend` shows state `UP` | Prometheus targets screen showing green `UP` target | **Verified App Metric API** |
| **18** | Grafana dashboard created | `monitoring/grafana/dashboards/fa2-dashboard.json` | Browser `http://localhost:3000/dashboards` | Dashboard "FA2 DevOps Observability Dashboard" opens | Grafana dashboard interface showing provisioned dashboard | **Verified Provisioning Config** |
| **19** | 2+ meaningful metrics visualized | `monitoring/grafana/dashboards/fa2-dashboard.json` | Browser `http://localhost:3000` | Graphs update when clicking frontend "Test Backend API" | Grafana panels showing live request counts and rate | **Verified Panel PromQL** |
| **20** | README explains pipeline, k8s, monitoring | `README.md`, `docs/FINAL_SETUP_GUIDE.md` | Open `README.md` and `docs/FINAL_SETUP_GUIDE.md` | Comprehensive documentation, architecture, rubric mapping | Markdown documentation view in browser/IDE | **Verified Complete** |
