import os
import time
from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Histogram, Info, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Application Metadata Info Metric
APP_INFO = Info("app_info", "DevOps FA2 Application Metadata")
APP_INFO.info({
    "app_name": "fa2-backend",
    "version": "2.0.0",
    "environment": os.getenv("ENVIRONMENT", "unknown")
})

# Prometheus Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests processed by backend",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Latency in Seconds",
    ["method", "endpoint"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

ITEMS_CREATED = Counter(
    "items_created_total",
    "Total items created via API (Business Metric)"
)

# In-memory storage for items demo
items_db = [
    {"id": 1, "name": "DevOps Starter", "description": "FA1 baseline service"},
    {"id": 2, "name": "Observability Stack", "description": "Prometheus and Grafana configured"}
]

@app.before_request
def before_request_hook():
    request.start_time = time.time()

@app.after_request
def after_request_hook(response):
    # Avoid double-counting if an error occurred before start_time
    latency = 0.0
    if hasattr(request, "start_time"):
        latency = time.time() - request.start_time

    # Safe, bounded endpoint label
    endpoint = request.endpoint or "unmapped"
    status_code = str(response.status_code)

    # Don't record internal metric endpoint metrics inside request counter to avoid scraping loops
    if request.path != "/metrics":
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=status_code).inc()
        REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(latency)

    return response

@app.route("/")
def home():
    return jsonify({
        "message": "Backend API is running",
        "environment": os.getenv("ENVIRONMENT", "unknown")
    })

@app.route("/api/hello")
def hello():
    return jsonify({
        "message": "Hello from the DevOps Backend!",
        "environment": os.getenv("ENVIRONMENT", "unknown")
    })

@app.route("/health")
@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "backend",
        "environment": os.getenv("ENVIRONMENT", "unknown")
    }), 200

@app.route("/api/items", methods=["GET"])
def get_items():
    return jsonify({
        "items": items_db,
        "count": len(items_db)
    }), 200

@app.route("/api/items", methods=["POST"])
def create_item():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    name = data.get("name")
    if not name or not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Field 'name' is required and must not be empty"}), 400

    description = data.get("description", "").strip() if isinstance(data.get("description"), str) else ""

    new_item = {
        "id": len(items_db) + 1,
        "name": name.strip(),
        "description": description
    }
    items_db.append(new_item)
    ITEMS_CREATED.inc()

    return jsonify(new_item), 201

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)