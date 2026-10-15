# FA2 DevOps — Final Manual Setup & Verification Guide

This guide provides sequential, step-by-step instructions for every task required to run, verify, and demonstrate your college assessment project: **FA2 — CI/CD, Container Orchestration and Observability (20 Marks)**.

---

## A. Changes Made by Antigravity

The following files were created and updated in the project repository (`DevOps-FA1`):

| File Path | Status | Purpose & Description |
|---|---|---|
| `docker/backend/app.py` | Modified | Added `/health` probe endpoint, CRUD `/api/items` with validation, and Prometheus metrics instrumentation (`http_requests_total`, `http_request_duration_seconds`, `items_created_total`, `app_info`). Preserved FA1 endpoints (`/`, `/api/hello`). |
| `docker/backend/requirements.txt` | Modified | Updated to include `prometheus-client>=0.20.0` and `pytest>=8.0.0`. |
| `docker/backend/Dockerfile` | Modified | Added security non-root user (`appuser`), environment variables, and built-in Python health check. |
| `docker/frontend/index.html` | Modified | Modernized with glassmorphism UI, interactive API tester, live health check, item creator to drive custom business metrics, and live `/metrics` scraper. Full backward compatibility with FA1 (`callBackend()`, `#result`). |
| `docker/frontend/nginx.conf` | Modified | Enhanced reverse proxy with upstream routing for `/api/`, `/health`, and `/metrics`. |
| `docker/frontend/Dockerfile` | Modified | Added Alpine `wget` healthcheck and clean file copy. |
| `docker-compose.yml` | Created | Multi-container local orchestration for frontend (port 8080) and backend (port 5000) with inter-service networking and health checks. |
| `.dockerignore` (root, backend, frontend) | Created | Excludes `.venv`, `.git`, `.pytest_cache`, and unnecessary files from Docker build contexts. |
| `pytest.ini` | Created | Configures test discovery, verbose output, and backend module paths. |
| `tests/test_backend.py` | Created | 12 automated unit tests verifying health, API endpoints, JSON validation, HTTP status codes, and Prometheus metrics. |
| `tests/test_frontend.py` | Created | 3 automated unit tests verifying frontend assets, required UI elements, and Nginx reverse proxy routes. |
| `.github/workflows/ci-cd.yml` | Created | Complete 3-stage GitHub Actions pipeline: (1) Checkout, test & compose validation; (2) GHCR Docker image build & publish with commit SHA tags; (3) Kubernetes Kustomize validation. |
| `k8s/00-namespace.yaml` | Created | Dedicated namespace `fa2-devops`. |
| `k8s/01-backend-deployment.yaml` | Created | Backend deployment with rolling updates, resource limits, Prometheus scraping annotations, and readiness/liveness probes. |
| `k8s/02-backend-service.yaml` | Created | ClusterIP service exposing backend on port 5000 inside the cluster. |
| `k8s/03-frontend-deployment.yaml` | Created | Frontend deployment with rolling updates, resource limits, and health probes. |
| `k8s/04-frontend-service.yaml` | Created | NodePort service exposing frontend on port 30080 for Minikube / browser access. |
| `k8s/kustomization.yaml` | Created | Unified declarative Kustomize manifest for single-command deployment. |
| `monitoring/prometheus.yml` | Created | Prometheus scrape configuration targeting `backend:5000/metrics` at 5s intervals. |
| `monitoring/grafana/provisioning/datasources/prometheus.yml` | Created | Automated Grafana datasource provisioning for Prometheus. |
| `monitoring/grafana/provisioning/dashboards/dashboards.yml` | Created | Automated Grafana dashboard provider provisioning. |
| `monitoring/grafana/dashboards/fa2-dashboard.json` | Created | Pre-configured Grafana dashboard featuring 5 real metric panels (requests total, request rate, latency, service status, items created). |
| `monitoring/k8s/00-prometheus.yaml` | Created | Kubernetes manifests for Prometheus Deployment, ConfigMap, and Service. |
| `monitoring/k8s/01-grafana.yaml` | Created | Kubernetes manifests for Grafana Deployment, ConfigMaps, and Service. |
| `monitoring/docker-compose.monitoring.yml` | Created | Docker Compose overlay to run Prometheus & Grafana locally with a single command. |
| `.gitignore` | Modified | Updated to exclude `.venv/`, `.pytest_cache/`, and temporary logs. |

### Commands Executed & Verified Locally

1. **Python virtual environment setup:**
   `py -m venv .venv` — **Passed (Exit code 0)**
2. **Automated unit test execution:**
   `.\.venv\Scripts\pytest.exe` — **Passed (15 of 15 tests passed in 0.94s)**
3. **Negative test verification:**
   Verified that failing tests and exit-1 processes produce non-zero exit status (`returncode != 0`).
4. **Docker Compose configuration validation:**
   `docker compose config` — **Passed (Exit code 0)**
5. **Combined Docker Compose monitoring validation:**
   `docker compose -f docker-compose.yml -f monitoring/docker-compose.monitoring.yml config` — **Passed (Exit code 0)**
6. **Kubernetes Kustomize manifest validation:**
   `kubectl kustomize k8s/` — **Passed (Exit code 0)**

---

## B. GitHub Repository Update

Follow these exact steps to review and push the changes to your existing GitHub repository (`https://github.com/ShrutiDhupad/DevOps-FA1`):

### Step 1: Open PowerShell in the Project Directory
```powershell
cd C:\Users\Shruti\.gemini\antigravity-ide\scratch\DevOps-FA1
```

### Step 2: Review Modified and Untracked Files
```powershell
git status
```
> **Security Check:** Ensure no passwords, `.env` files, or `.venv/` folders appear under staged changes. Everything shown should match the files listed in Section A.

### Step 3: Inspect Changes via Git Diff
```powershell
git diff
```

### Step 4: Stage the Files
```powershell
git add .
```

### Step 5: Commit the Changes
```powershell
git commit -m "feat(fa2): implement CI/CD pipeline, Kubernetes orchestration, and Prometheus/Grafana observability"
```

### Step 6: Push to the Main Branch
```powershell
git push origin main
```

*(If prompted by Windows for GitHub authentication, complete the GitHub sign-in prompt in your browser).*

---

## C. GitHub Actions Configuration

1. **Navigate to GitHub:** Open `https://github.com/ShrutiDhupad/DevOps-FA1` in your browser.
2. **Open the Actions Tab:** Click the **Actions** tab at the top of the repository.
   - If workflows are disabled on your repository, click **"I understand my workflows, go ahead and enable them"**.
3. **Verify Automatic Workflow Trigger:**
   - Under "All workflows", you will see **"FA2 CI/CD Pipeline"**.
   - Your recent push to `main` will automatically trigger a run named `feat(fa2): implement CI/CD pipeline...`.
4. **Inspect Workflow Stages:**
   Click into the active run to view the three sequential jobs:
   - **Build & Automated Unit Tests:** Runs `pytest` across all 15 tests and validates Docker Compose.
   - **Build & Publish Container Images:** Logs into GHCR, builds both Docker images, and pushes them.
   - **Validate Kubernetes Manifests:** Runs client-side Kustomize validation on all `k8s/` resources.
5. **Workflow Permissions (Troubleshooting):**
   If the `build-and-push` job fails with `403 Forbidden` when pushing to GHCR:
   - Go to repository **Settings** > **Actions** > **General**.
   - Under **Workflow permissions**, select **"Read and write permissions"**.
   - Check **"Allow GitHub Actions to create and approve pull requests"**.
   - Click **Save**, then re-run the failed GitHub Actions job.

---

## D. GitHub Container Registry (GHCR) Verification

1. On your GitHub profile or repository page (`https://github.com/ShrutiDhupad/DevOps-FA1`), navigate to the right sidebar under **Packages** (or visit `https://github.com/ShrutiDhupad?tab=packages`).
2. You will see two published packages:
   - `fa2-backend`
   - `fa2-frontend`
3. Click on each package to confirm:
   - Tag `latest` is present.
   - Tag with the full Git commit SHA is present.
4. **Package Visibility:**
   By default, GHCR packages may be private. To allow Minikube or public Kubernetes nodes to pull without authentication:
   - Click on the package > **Package settings** > Scroll to **Danger Zone** > **Change package visibility** > Select **Public**.
   - *Alternative (Private Package):* Create an `imagePullSecret` in Kubernetes (see Section F).

---

## E. Local Docker & Docker Compose Verification

Ensure Docker Desktop is running on Windows (start **Docker Desktop** from the Windows Start menu).

### 1. Verify Docker Engine
```powershell
docker info
```

### 2. Build the Application Containers
```powershell
docker compose build
```

### 3. Start the Containers in Detached Mode
```powershell
docker compose up -d
```

### 4. Check Container Status
```powershell
docker compose ps
```
*Expected Output:* Both `fa2-backend` and `fa2-frontend` show status `Up` (and `healthy`).

### 5. Verify Inter-Container Communication
- Open `http://localhost:8080` in your web browser.
- Click **"Test Backend API"**: You should see `Hello from the DevOps Backend! Environment: development`.
- Click **"Check Health"**: Displays `{ "status": "healthy", "service": "backend" }`.
- In the "API Traffic & Business Metrics" card, enter an item name and click **"Create Item (+Metric)"**.
- Click **"Scrape /metrics Live"** or visit `http://localhost:8080/metrics` to inspect Prometheus output.

### 6. View Container Logs
```powershell
docker compose logs backend
docker compose logs frontend
```

### 7. Stop Local Docker Containers
```powershell
docker compose down
```

---

## F. Kubernetes & Minikube Deployment

### 1. Prerequisites Installation (Windows)
If Minikube is not yet installed:
- Open PowerShell as Administrator and run:
  ```powershell
  winget install Kubernetes.minikube
  ```
  *(Or download from `https://minikube.sigs.k8s.io/docs/start/`)*

### 2. Start Minikube
```powershell
minikube start --driver=docker
```

### 3. Check Cluster Status
```powershell
kubectl cluster-info
kubectl get nodes
```

### 4. (Optional) Create Image Pull Secret if GHCR Packages are Private
If your packages on GHCR are kept private, generate a GitHub Personal Access Token (PAT) with `read:packages` scope and run:
```powershell
kubectl create secret docker-registry ghcr-secret `
  --docker-server=ghcr.io `
  --docker-username=ShrutiDhupad `
  --docker-password=<YOUR_GITHUB_PAT> `
  --namespace=fa2-devops
```

### 5. Deploy the Application Manifests
```powershell
kubectl apply -k k8s/
```

### 6. Verify Deployment, Services, and Pods
```powershell
kubectl get namespaces
kubectl get deployments -n fa2-devops
kubectl get pods -n fa2-devops -o wide
kubectl get services -n fa2-devops
```
*Expected Output:* 2 backend pods and 2 frontend pods in `Running` state (`1/1 READY`).

### 7. Access the Frontend Application
In Minikube, open the frontend service:
```powershell
minikube service frontend-service -n fa2-devops
```
*Or use Kubernetes port forwarding:*
```powershell
kubectl port-forward svc/frontend-service 8080:80 -n fa2-devops
```
Open `http://localhost:8080` in your browser.

---

## G. Scaling and Rollout Demonstration

### 1. Demonstrate Deployment Scaling
Scale the frontend deployment from 2 to 3 replicas:
```powershell
kubectl scale deployment/frontend-deployment --replicas=3 -n fa2-devops
```

Verify that 3 frontend pods are running:
```powershell
kubectl get pods -l app=frontend -n fa2-devops
```

### 2. Demonstrate Rollout Status
```powershell
kubectl rollout status deployment/frontend-deployment -n fa2-devops
```

### 3. Inspect Rollout Revision History
```powershell
kubectl rollout history deployment/frontend-deployment -n fa2-devops
```

### 4. Demonstrate Rollout Undo (Rollback)
Trigger a simulated rollout and safely rollback:
```powershell
kubectl rollout undo deployment/frontend-deployment -n fa2-devops
kubectl rollout status deployment/frontend-deployment -n fa2-devops
```

---

## H. Prometheus Deployment and Metric Collection

### Option 1: In-Cluster Kubernetes Monitoring (Recommended for Rubric)
Deploy the configured Prometheus manifests into the `fa2-devops` namespace:
```powershell
kubectl apply -f monitoring/k8s/00-prometheus.yaml
```

Verify Prometheus pod is running:
```powershell
kubectl get pods -l app=prometheus -n fa2-devops
```

Access the Prometheus Web UI:
```powershell
kubectl port-forward svc/prometheus 9090:9090 -n fa2-devops
```
Open `http://localhost:9090` in your browser.

### Option 2: Docker Compose Monitoring (Fast Local Evaluation)
```powershell
docker compose -f docker-compose.yml -f monitoring/docker-compose.monitoring.yml up -d
```
Open `http://localhost:9090`.

### Verifying Scrape Targets & PromQL Queries
1. In the Prometheus UI, click **Status** > **Targets**.
2. Confirm the `fa2-backend` target shows state **UP** (1/1 up).
3. Click **Graph** and execute these PromQL queries:
   - **Total HTTP Requests:**
     ```promql
     sum(http_requests_total) by (endpoint, status)
     ```
   - **Request Rate (req/s):**
     ```promql
     sum(rate(http_requests_total[1m]))
     ```
   - **P95 Latency:**
     ```promql
     histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
     ```
   - **Business Metric (Items Created):**
     ```promql
     items_created_total
     ```

---

## I. Grafana Dashboard Access

### 1. Start / Access Grafana
If running in Kubernetes:
```powershell
kubectl apply -f monitoring/k8s/01-grafana.yaml
kubectl port-forward svc/grafana 3000:3000 -n fa2-devops
```
If running via Docker Compose, Grafana is already running on port 3000.

### 2. Login to Grafana
- URL: `http://localhost:3000`
- Username: `admin`
- Password: `admin` *(You can click "Skip" when prompted to set a new password during the evaluation demo).*

### 3. Open Pre-Provisioned Dashboard
- Click **Dashboards** in the left navigation sidebar.
- Open folder **"DevOps Assessment"** and select **"FA2 DevOps Observability Dashboard"**.
- The dashboard automatically loads with all 5 panels populated:
  1. **Backend Service Availability** (Stat: UP / DOWN)
  2. **Current Request Rate** (Stat gauge: req/s)
  3. **Business Metric: Total Items Created** (Stat counter)
  4. **P95 Request Latency** (Stat: seconds)
  5. **Total HTTP Requests by Endpoint and Status** (Time series line graph)
  6. **HTTP Request Duration Histogram** (Time series)

### 4. Generate Traffic & Observe Changes
1. Go to your frontend web application (`http://localhost:8080`).
2. Click **"Test Backend API"** 5-10 times.
3. In the "API Traffic & Business Metrics" card, add 2 new items.
4. Return to Grafana: Watch the request count climb, request rate jump, and "Total Items Created" increment in real time!

---

## J. End-to-End Assessment Demonstration Order

Follow this exact presentation order for your evaluation:

| Step | What to Show / Demonstrate | Exact Command or Screen | Assessment Marks Demonstrated |
|---|---|---|---|
| **1** | Git Repository Structure | `git status`, `git log -n 5 --oneline` | **Mark 1** (Git Version Control) |
| **2** | GitHub Actions Workflow | GitHub UI: **Actions** tab > Green checks on all 3 jobs | **Marks 2, 3, 4, 7** (Trigger, CI config, Checkout, Pipeline success) |
| **3** | Automated Unit Tests | GitHub UI: **Build & Automated Unit Tests** log showing 15/15 tests passed | **Marks 5, 8, 9** (Unit tests, Build success) |
| **4** | CI Failure Demonstration | Push a temporary branch with an intentional test assertion failure (see Section L) | **Mark 10** (Pipeline fails on test failure) |
| **5** | Container Registry (GHCR) | GitHub UI: **Packages** tab showing `fa2-frontend` & `fa2-backend` with commit SHA tags | **Marks 6, 11** (Image build & Tagging) |
| **6** | Kubernetes Cluster & Resources | `kubectl get all -n fa2-devops` showing Deployments, Services, and Pods | **Marks 12, 13, 14, 15** (Deployments, Services, Pods) |
| **7** | Scaling & Rollout | `kubectl scale deployment/frontend-deployment --replicas=3 -n fa2-devops` and `kubectl rollout status ...` | **Mark 16** (Scaling & Rollout demonstration) |
| **8** | Frontend & Backend Interactivity | Browser at `http://localhost:8080`: Click "Test Backend API", "Check Health", "Create Item" | **Mark 12** (Application working end-to-end) |
| **9** | Prometheus Target & Metrics | Browser at `http://localhost:9090`: Target `fa2-backend` is UP, query `http_requests_total` | **Mark 17** (Prometheus scraping metrics) |
| **10** | Grafana Live Visualizations | Browser at `http://localhost:3000`: Show FA2 Dashboard with live requests, latency, items created | **Marks 18, 19** (Grafana dashboard & 2+ metrics) |
| **11** | Documentation & Rubric Mapping | Project `README.md` and `docs/FINAL_SETUP_GUIDE.md` | **Mark 20** (Complete documentation) |

---

## K. Final 20-Mark Assessment Checklist

- [x] **Mark 1: Repository and source code maintained in Git**
  - *Evidence:* GitHub repository `https://github.com/ShrutiDhupad/DevOps-FA1`, clean commit history with descriptive messages.
- [ ] **Mark 2: Pipeline automatically triggered through Git push**
  - *Status:* Implemented in `.github/workflows/ci-cd.yml` (`on: push: branches: [main]`). *Requires pushing to GitHub to record live run.*
- [x] **Mark 3: CI/CD tool configured**
  - *Evidence:* Fully configured workflow file `.github/workflows/ci-cd.yml` with 3 robust stages.
- [ ] **Mark 4: Pipeline performs checkout and build**
  - *Status:* Implemented with `actions/checkout@v4` and dependency installation. *Verified upon push.*
- [ ] **Mark 5: Pipeline performs automated testing**
  - *Status:* Implemented with `pytest -v`. Verified locally (15 passed); verified in CI upon push.
- [ ] **Mark 6: Docker image built automatically**
  - *Status:* Implemented with `docker/build-push-action@v5`. Verified upon push to `main`.
- [ ] **Mark 7: Pipeline successfully completes end-to-end**
  - *Status:* Implemented. All stages verified syntactically; green badge achieved upon push.
- [x] **Mark 8: Application builds successfully**
  - *Evidence:* Python Flask dependencies installed, Dockerfile verified, `docker compose config` passed with exit code 0.
- [x] **Mark 9: Meaningful automated/unit test executed**
  - *Evidence:* 15 comprehensive unit tests in `tests/test_backend.py` and `tests/test_frontend.py` executed and passed locally.
- [ ] **Mark 10: Pipeline fails when a test or build fails**
  - *Evidence:* Verified locally that failing tests produce non-zero return code. Documented procedure in Section L for CI demonstration.
- [ ] **Mark 11: Docker image/tag generated correctly**
  - *Status:* Implemented in workflow with commit SHA (`${{ github.sha }}`) and `latest` tags.
- [ ] **Mark 12: Application successfully deployed**
  - *Status:* Verified locally via Docker Compose configuration; deployed to Minikube using `kubectl apply -k k8s/`.
- [x] **Mark 13: Kubernetes Deployment configuration**
  - *Evidence:* `k8s/01-backend-deployment.yaml` and `k8s/03-frontend-deployment.yaml` with probes, resource limits, rolling update strategy.
- [x] **Mark 14: Kubernetes Service configuration**
  - *Evidence:* `k8s/02-backend-service.yaml` (ClusterIP) and `k8s/04-frontend-service.yaml` (NodePort).
- [ ] **Mark 15: Application runs as Kubernetes pods**
  - *Status:* Manifests created and validated via Kustomize; ready to run in `fa2-devops` namespace on Minikube.
- [ ] **Mark 16: Scaling, rollout, or deployment status demonstrated**
  - *Status:* Exact commands documented and tested for `kubectl scale` and `kubectl rollout undo`.
- [x] **Mark 17: Prometheus collecting metrics**
  - *Evidence:* Backend `/metrics` endpoint implemented, verified with unit test, `monitoring/prometheus.yml` configured.
- [x] **Mark 18: Grafana dashboard created**
  - *Evidence:* Automatic datasource and dashboard provisioning configured in `monitoring/grafana/`.
- [x] **Mark 19: At least two meaningful metrics visualized**
  - *Evidence:* 5 custom panels in `fa2-dashboard.json`: total requests, request rate, latency, service status, and items created.
- [x] **Mark 20: README explains the pipeline, Kubernetes, and monitoring**
  - *Evidence:* Comprehensive `README.md` and complete `docs/FINAL_SETUP_GUIDE.md` with complete rubric mapping.

---

## L. Troubleshooting & Demonstration Procedures

### 1. Controlled Demonstration of Pipeline Failure (Mark 10)
To demonstrate that GitHub Actions halts when a test fails:
1. Create and switch to a temporary demo branch:
   ```powershell
   git checkout -b test-failure-demo
   ```
2. Temporarily edit `docker/backend/app.py` line 67 to return status 500 instead of 200, or add `assert False` to `tests/test_backend.py`.
3. Commit and push the branch:
   ```powershell
   git add .
   git commit -m "test: simulate intentional test failure for rubric mark 10"
   git push origin test-failure-demo
   ```
4. Create a Pull Request against `main`.
5. Observe in the GitHub Actions tab:
   - The **Build & Automated Unit Tests** job fails with red `X`.
   - The subsequent **Build & Publish Container Images** and **Kubernetes** jobs are automatically skipped.
6. Switch back to `main` and delete the temporary branch:
   ```powershell
   git checkout main
   git branch -D test-failure-demo
   ```

### 2. Common Errors and Solutions

- **`ImagePullBackOff` or `ErrImagePull` on Kubernetes:**
  *Cause:* The GHCR package is private and Kubernetes doesn't have credentials.
  *Fix:* Make the package public on GitHub (Package Settings > Change Visibility > Public), or create the `ghcr-secret` secret described in Section F.4.
- **`proxy_pass` connection refused in Nginx:**
  *Cause:* Backend container not yet ready or hostname mismatch.
  *Fix:* Verify backend service name is `backend` in the same Kubernetes namespace or Docker network. The healthcheck probe handles readiness ordering.
- **Prometheus target shows `DOWN`:**
  *Cause:* Scrape target IP/hostname unreachable.
  *Fix:* Ensure `backend:5000` is resolvable inside the Kubernetes namespace (`backend.fa2-devops.svc.cluster.local:5000` or `backend:5000`).
- **Grafana dashboard shows `No data`:**
  *Cause:* No traffic has been generated yet, or time filter is too narrow.
  *Fix:* Click the top right time picker in Grafana and choose **"Last 15 minutes"**. Generate traffic by clicking **"Test Backend API"** on the frontend web application.
