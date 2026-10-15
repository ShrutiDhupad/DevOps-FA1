import os
import re
import pytest

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docker", "frontend"))

def test_frontend_files_exist():
    """Verify frontend static and configuration assets exist."""
    assert os.path.isfile(os.path.join(FRONTEND_DIR, "index.html"))
    assert os.path.isfile(os.path.join(FRONTEND_DIR, "nginx.conf"))
    assert os.path.isfile(os.path.join(FRONTEND_DIR, "Dockerfile"))

def test_frontend_index_html_structure():
    """Verify index.html contains essential FA1 and FA2 elements and IDs."""
    html_path = os.path.join(FRONTEND_DIR, "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # FA1 Backward Compatibility checks
    assert 'id="result"' in content
    assert "callBackend" in content
    assert "Test Backend API" in content

    # FA2 Enhancement checks
    assert 'id="btn-check-health"' in content
    assert 'id="btn-create-item"' in content
    assert 'id="item-name-input"' in content
    assert 'id="btn-view-metrics"' in content
    assert "/metrics" in content

def test_nginx_proxy_configuration():
    """Verify nginx.conf properly proxies backend API, health, and metrics."""
    nginx_path = os.path.join(FRONTEND_DIR, "nginx.conf")
    with open(nginx_path, "r", encoding="utf-8") as f:
        config = f.read()

    assert "listen 80;" in config
    assert "location /api/" in config
    assert "proxy_pass http://backend:5000/api/;" in config
    assert "location /health" in config
    assert "proxy_pass http://backend:5000/health;" in config
    assert "location /metrics" in config
    assert "proxy_pass http://backend:5000/metrics;" in config
