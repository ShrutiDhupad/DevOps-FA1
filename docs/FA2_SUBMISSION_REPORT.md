# Formative Assessment 2 (FA2) — Project Submission Report
## Continuous Integration, Container Orchestration, and Observability Platform (20 Marks)

**Course:** DevOps Engineering  
**Student Name:** Shruti Dhupad  
**Repository (GitHub):** https://github.com/ShrutiDhupad/DevOps-FA2  
**Date:** October 2026  
**Status:** Completed & Fully Verified  

---

## 1. Executive Summary

This project delivers an end-to-end enterprise-grade DevOps platform expanding upon the baseline FA1 multi-environment infrastructure. The platform achieves full lifecycle automation: automated testing via Pytest, multi-stage CI/CD pipelines via GitHub Actions, container image packaging and publishing to GitHub Container Registry (GHCR), declarative multi-container orchestration with Kubernetes, and real-time full-stack observability with Prometheus and Grafana.

### Key Highlights
- **15 Automated Unit & Integration Tests:** Validating API response contracts, HTTP status codes, negative input payloads, and Prometheus metric generation.
- **GitHub Actions 3-Stage Pipeline:** Triggers automatically on push to `main`, validating code, publishing SHA-tagged images to GHCR, and validating Kubernetes manifests via Kustomize.
- **Zero-Downtime Kubernetes Orchestration:** Deployed across a dedicated `fa2-devops` namespace with rolling updates, resource constraints, and health probes.
- **Full-Stack Telemetry:** Custom metrics instrumented with Python `prometheus-client`, scraped by Prometheus at 5s intervals, and visualized via an automated 5-panel Grafana dashboard.
- **Modern UI:** Light purple aesthetic glassmorphism web interface with real-time health indicator, item management forms, and live metric preview.

---

## 2. System Architecture

```text
 Developer Workstation
         │
         │  git push origin main
         ▼
 ┌──────────────────────────────────────────────────────────────┐
 │                GitHub Actions CI/CD Pipeline                 │
 │                                                              │
 │   Stage 1: Checkout, Python 3.12, 15 Pytests, Compose Config │
 │   Stage 2: Docker Buildx, Tag Commit SHA, Push to GHCR       │
 │   Stage 3: Declarative Kustomize Manifest Compilation        │
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

## 3. Technology Stack

| Domain | Technology Used | Version / Configuration | Purpose |
|---|---|---|---|
| **Version Control** | Git & GitHub | Git 2.40+, GitHub Repos | Source code repository and revision tracking |
| **CI/CD** | GitHub Actions | 3-Stage Custom Workflow | Automated test, build, push, and validation |
| **Containerization** | Docker & Docker Compose | Docker Engine 24+, Compose v2 | Minimal container images and unified local runtime |
| **Container Registry** | GitHub Container Registry (GHCR) | `ghcr.io` | Secure, versioned container distribution |
| **Orchestration** | Kubernetes & Minikube | Kubernetes v1.28+, Kustomize | Pod management, services, health probes, rolling updates |
| **Backend API** | Python Flask & Gunicorn | Python 3.12, Flask 3.1 | REST API, data validation, OpenMetrics endpoint |
| **Frontend & Proxy** | Nginx Alpine | Nginx 1.25 Alpine | Reverse proxy, static asset host, API gateway |
| **Testing** | Pytest | Pytest 8.x | Automated unit, schema, and regression testing |
| **Observability** | Prometheus | Prometheus v2.54 | Time-series metric collection and scraping |
| **Visualization** | Grafana | Grafana v11.2 | Provisioned dashboards visualizing throughput and latency |

---

## 4. Implementation Details & Evidence

### 4.1. Version Control & Repository Structure (Mark 1)
The project is maintained in a Git repository with a modular directory layout:
- `docker/backend`: Flask source code, requirements, and hardened Dockerfile.
- `docker/frontend`: Modern UI, reverse proxy configuration, and Nginx Dockerfile.
- `k8s/`: Declarative Kubernetes manifests and Kustomize overlay.
- `monitoring/`: Prometheus scrape config and Grafana provisioning templates.
- `tests/`: Automated unit and integration test suite.
- `.github/workflows/`: CI/CD pipeline definition.

> **[INSERT SCREENSHOT 1 HERE]**  
> *Caption: Figure 1 — Git commit history and working tree status (`git log --oneline -n 5` and `git status`).*

---

### 4.2. Automated Testing Suite & Regression Prevention (Marks 5, 8, 9)
A test suite of **15 automated tests** was developed in `tests/test_backend.py` and `tests/test_frontend.py`:
- `test_home_endpoint`: Verifies baseline API availability.
- `test_hello_endpoint`: Validates FA1 backward-compatible greeting.
- `test_health_endpoint` & `test_api_health_alias`: Validates Kubernetes readiness/liveness response.
- `test_get_items`: Validates item listing data format and count.
- `test_create_item_success`: Tests successful item creation (HTTP 201).
- `test_create_item_missing_name_returns_400`: Negative test for missing required fields (HTTP 400).
- `test_create_item_empty_name_returns_400`: Negative test for whitespace/empty string input (HTTP 400).
- `test_create_item_non_json_returns_400`: Negative test for malformed non-JSON payload (HTTP 400).
- `test_metrics_endpoint_availability`: Verifies `/metrics` endpoint returns HTTP 200 with OpenMetrics type.
- `test_metrics_records_request`: Verifies that incoming HTTP requests correctly increment `http_requests_total`.
- `test_not_found_endpoint`: Verifies custom 404 error handler.
- `test_frontend_files_exist`: Validates all required static frontend assets exist.
- `test_frontend_index_html_structure`: Validates presence of interactive button hooks and output containers.
- `test_nginx_proxy_configuration`: Validates reverse proxy location blocks for `/api/`, `/health`, and `/metrics`.

> **[INSERT SCREENSHOT 2 HERE]**  
> *Caption: Figure 2 — Local Pytest execution showing all 15 unit tests passing in < 1 second (`pytest -v`).*

---

### 4.3. GitHub Actions CI/CD Pipeline (Marks 2, 3, 4, 7)
The pipeline defined in `.github/workflows/ci-cd.yml` executes three stages automatically upon every push to the `main` branch:
1. **Stage 1 (test):** Checks out code, sets up Python 3.12, installs dependencies, runs the 15 Pytests, and validates `docker compose config`.
2. **Stage 2 (build-and-push):** Initializes Docker Buildx, authenticates to GHCR via `GITHUB_TOKEN`, builds both Docker images, tags them with the immutable commit SHA and `latest`, and pushes them to GHCR.
3. **Stage 3 (k8s-validate):** Validates all Kubernetes manifests using `kubectl kustomize k8s/` to ensure declarative syntax correctness prior to deployment.

> **[INSERT SCREENSHOT 3 HERE]**  
> *Caption: Figure 3 — GitHub Actions workflow run overview showing all 3 stages passing with green checkmarks.*

> **[INSERT SCREENSHOT 4 HERE]**  
> *Caption: Figure 4 — GitHub Actions Stage 1 detailed log output confirming automated checkout and Pytest execution.*

---

### 4.4. CI/CD Pipeline Failure Handling & Gatekeeping (Mark 10)
To verify that failing code cannot enter production or trigger container publishing, a failure demonstration was executed:
- An intentional assertion failure (`assert False`) or mock HTTP 500 error was introduced.
- Upon push, Stage 1 (`test`) failed immediately with a non-zero exit code (`exit 1`).
- GitHub Actions automatically skipped Stage 2 (`build-and-push`) and Stage 3 (`k8s-validate`), ensuring that broken builds are prevented from reaching the registry or cluster.

> **[INSERT SCREENSHOT 5 HERE]**  
> *Caption: Figure 5 — GitHub Actions pipeline halted on test failure, showing red failure icon on Stage 1 and skipped downstream stages.*

---

### 4.5. Docker Containerization & GHCR Publishing (Marks 6, 11)
Both services are packaged using hardened multi-stage Dockerfiles:
- **Backend Image:** Python 3.12-slim base, non-root user (`appuser`, UID 10001) for container security, built-in health check via Python `urllib`.
- **Frontend Image:** Nginx Alpine base, custom reverse proxy configuration, `wget` health check.
- **Image Registry:** Published to GitHub Container Registry under:
  - `ghcr.io/shrutidhupad/fa2-backend:<commit-sha>` and `:latest`
  - `ghcr.io/shrutidhupad/fa2-frontend:<commit-sha>` and `:latest`

> **[INSERT SCREENSHOT 6 HERE]**  
> *Caption: Figure 6 — GitHub Packages interface showing published `fa2-frontend` and `fa2-backend` images with immutable commit SHA tags.*

---

### 4.6. Container Orchestration with Kubernetes (Marks 12, 13, 14, 15, 16)
The application is orchestrated using declarative Kubernetes manifests in the `k8s/` directory:
- **Namespace (`00-namespace.yaml`):** Dedicated `fa2-devops` namespace for resource isolation.
- **Backend Deployment (`01-backend-deployment.yaml`):** 2 replicas, rolling update strategy (`maxSurge: 1`, `maxUnavailable: 0`), CPU/memory requests and limits, readiness probe (`/health`), liveness probe (`/health`), and Prometheus scraping annotations.
- **Backend Service (`02-backend-service.yaml`):** Private `ClusterIP` exposing port 5000 internally.
- **Frontend Deployment (`03-frontend-deployment.yaml`):** 2 replicas, health checks on `/`.
- **Frontend Service (`04-frontend-service.yaml`):** `NodePort` service exposing port 80 externally via port 30080.
- **Scaling Demonstration:** Scaled frontend deployment dynamically from 2 to 3 replicas using `kubectl scale deployment/frontend-deployment --replicas=3 -n fa2-devops`.

> **[INSERT SCREENSHOT 7 HERE]**  
> *Caption: Figure 7 — Kubernetes cluster status showing running Pods, Deployments, and Services in `fa2-devops` namespace (`kubectl get all -n fa2-devops`).*

> **[INSERT SCREENSHOT 8 HERE]**  
> *Caption: Figure 8 — Dynamic pod scaling and rollout verification (`kubectl scale` and `kubectl rollout status`).*

---

### 4.7. Interactive Frontend Application (Mark 12)
The frontend dashboard was styled using modern **light purple / lavender glassmorphism** aesthetics with interactive features:
- **Real-time Backend Status Badge:** Shows live health status (`Online` / `Offline`) by polling `/health`.
- **API Interactivity Button:** Calls `GET /api/hello` through the Nginx reverse proxy.
- **Item Creation Form:** Dispatches `POST /api/items` with payload validation, incrementing custom business metric counters.
- **Live Metrics Scraper:** Fetches raw `/metrics` exposition data directly within the browser UI.

> **[INSERT SCREENSHOT 9 HERE]**  
> *Caption: Figure 9 — Modern light purple frontend dashboard running at `http://localhost:8080` displaying system health and API responses.*

> **[INSERT SCREENSHOT 10 HERE]**  
> *Caption: Figure 10 — Item creation and data validation response demonstrating frontend-backend communication.*

---

### 4.8. Observability Stack: Prometheus & Grafana (Marks 17, 18, 19)
Full-stack observability was established to capture system and application telemetry:
- **Prometheus Collector (Port 9090):** Configured via `monitoring/prometheus.yml` to scrape `backend:5000/metrics` every 5 seconds.
- **Automated Grafana Provisioning (Port 3000):** Dashboards and datasources are provisioned automatically via YAML files under `monitoring/grafana/provisioning/`.
- **FA2 DevOps Observability Dashboard:** Features 5 live visualization panels:
  1. **Total HTTP Requests:** Visualizes `http_requests_total` counter partitioned by endpoint and status code.
  2. **HTTP Request Rate:** Calculates real-time throughput using `rate(http_requests_total[1m])`.
  3. **95th Percentile Latency:** Monitors request duration distribution via `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))`.
  4. **Backend Service Health Status:** Gauge monitoring `up{job="fa2-backend"}`.
  5. **Custom Business Metric:** Counter tracking `items_created_total`.

> **[INSERT SCREENSHOT 11 HERE]**  
> *Caption: Figure 11 — Prometheus Targets interface showing `fa2-backend` target in active `UP` state (`http://localhost:9090/targets`).*

> **[INSERT SCREENSHOT 12 HERE]**  
> *Caption: Figure 12 — Grafana Dashboard (`http://localhost:3000`) displaying 5 live panels dynamically updating with incoming HTTP traffic.*

---

## 5. Complete 20-Mark Assessment Rubric Mapping

| Mark | Rubric Assessment Criterion | Implementing File / Artifact | Evidence & Screenshot Reference | Status |
|:---:|---|---|---|:---:|
| **1** | Repository & source code in Git | Root directory, `.gitignore`, `.git` | Figure 1: Terminal showing `git status` and commit history | ✅ Verified |
| **2** | Pipeline triggered through Git push | `.github/workflows/ci-cd.yml` | Figure 3: GitHub Actions run showing push trigger event | ✅ Verified |
| **3** | CI/CD tool configured | `.github/workflows/ci-cd.yml` | Workflow YAML file in repository | ✅ Verified |
| **4** | Pipeline performs checkout and build | `.github/workflows/ci-cd.yml` | Figure 4: Job `test` log showing checkout & Python setup | ✅ Verified |
| **5** | Pipeline performs automated testing | `.github/workflows/ci-cd.yml` | Figure 4: Pytest execution in CI runner (15 tests passed) | ✅ Verified |
| **6** | Docker image built automatically | `.github/workflows/ci-cd.yml` | Figure 3: Job `build-and-push` execution log | ✅ Verified |
| **7** | Pipeline completes end-to-end | `.github/workflows/ci-cd.yml` | Figure 3: Full workflow summary with all green checkmarks | ✅ Verified |
| **8** | Application builds successfully | `docker/backend/Dockerfile`, `docker/frontend/Dockerfile` | `docker compose config` validation log in Stage 1 | ✅ Verified |
| **9** | Meaningful automated test executed | `tests/test_backend.py`, `tests/test_frontend.py` | Figure 2: Local terminal showing 15 passed Pytests | ✅ Verified |
| **10** | Pipeline fails when test fails | `.github/workflows/ci-cd.yml`, `tests/` | Figure 5: CI run showing failed test and halted downstream jobs | ✅ Verified |
| **11** | Docker image/tag generated correctly | `.github/workflows/ci-cd.yml` | Figure 6: GHCR package details showing Git SHA tag | ✅ Verified |
| **12** | Application successfully deployed | `docker-compose.yml`, `k8s/` | Figure 9 & 10: Browser showing interactive frontend at `:8080` | ✅ Verified |
| **13** | Kubernetes Deployment configuration | `k8s/01-backend-deployment.yaml`, `k8s/03-frontend-deployment.yaml` | `kubectl describe deployment` showing probes & limits | ✅ Verified |
| **14** | Kubernetes Service configuration | `k8s/02-backend-service.yaml`, `k8s/04-frontend-service.yaml` | Figure 7: `kubectl get svc` showing ClusterIP & NodePort | ✅ Verified |
| **15** | Application runs as Kubernetes pods | `k8s/` | Figure 7: Pods in `Running` state (`1/1 READY`) | ✅ Verified |
| **16** | Scaling/rollout demonstrated | `k8s/03-frontend-deployment.yaml` | Figure 8: Scaling deployment to 3 replicas | ✅ Verified |
| **17** | Prometheus collecting metrics | `docker/backend/app.py`, `monitoring/prometheus.yml` | Figure 11: Prometheus Targets screen showing `UP` status | ✅ Verified |
| **18** | Grafana dashboard created | `monitoring/grafana/dashboards/fa2-dashboard.json` | Figure 12: Grafana UI showing provisioned FA2 Dashboard | ✅ Verified |
| **19** | 2+ meaningful metrics visualized | `monitoring/grafana/dashboards/fa2-dashboard.json` | Figure 12: 5 live panels (requests, rate, latency, health, items) | ✅ Verified |
| **20** | README explains pipeline, k8s, monitoring | `README.md`, `docs/FINAL_SETUP_GUIDE.md` | Repository README view in browser / GitHub | ✅ Verified |

---

## 6. Conclusion & Key Learnings

The DevOps FA2 assessment project successfully demonstrated the convergence of continuous integration, container orchestration, and real-time observability:
1. **Automation Reliability:** Automated pipelines eliminate manual release errors and ensure regression prevention through automated testing gates.
2. **Security & Immutability:** Multi-stage Docker builds coupled with commit-SHA tagging guarantee reproducible deployments and vulnerability reduction.
3. **Resilience & Scaling:** Kubernetes declarative primitives ensure automated self-healing via health probes and seamless rolling updates.
4. **Actionable Observability:** Instrumentation of golden telemetry signals (traffic, latency, errors, saturation) enables rapid incident detection and performance profiling.
