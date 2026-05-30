import pytest

from app import app


@pytest.fixture
def client():

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# ==========================================
# HEALTH CHECK
# ==========================================

def test_health_endpoint(client):

    response = client.get("/health")

    assert response.status_code == 200

    assert response.is_json

    data = response.get_json()

    assert data["status"] == "healthy"


# ==========================================
# DASHBOARD PAGE
# ==========================================

def test_dashboard_page(client):

    response = client.get("/dashboard")

    assert response.status_code == 200


# ==========================================
# LOGS PAGE
# ==========================================

def test_logs_page(client):

    response = client.get("/logs")

    assert response.status_code == 200


# ==========================================
# ALERTS PAGE
# ==========================================

def test_alerts_page(client):

    response = client.get("/alerts")

    assert response.status_code == 200


# ==========================================
# SERVERS PAGE
# ==========================================

def test_servers_page(client):

    response = client.get("/servers")

    assert response.status_code == 200


# ==========================================
# SETTINGS PAGE
# ==========================================

def test_settings_page(client):

    response = client.get("/settings")

    assert response.status_code == 200


# ==========================================
# SYSTEM API
# ==========================================

def test_system_api(client):

    response = client.get("/api/system")

    assert response.status_code == 200

    assert response.is_json

    data = response.get_json()

    assert "cpu" in data
    assert "memory" in data
    assert "disk" in data
    assert "hostname" in data


# ==========================================
# ALERTS API
# ==========================================

def test_alerts_api(client):

    response = client.get("/api/alerts")

    assert response.status_code == 200

    assert response.is_json


# ==========================================
# LOGS API
# ==========================================

def test_logs_api(client):

    response = client.get("/api/logs")

    assert response.status_code == 200

    assert response.is_json


# ==========================================
# DEPLOYMENTS API
# ==========================================

def test_deployments_api(client):

    response = client.get("/api/deployments")

    assert response.status_code == 200

    assert response.is_json

# ==========================================
# HEALTH LOGGING TEST
# ==========================================

def test_health_logging(client, caplog):

    with caplog.at_level("INFO"):

        response = client.get("/health")

        assert response.status_code == 200

        messages = [

            record.message

            for record in caplog.records

        ]

        assert any(

            "Health check requested" in msg

            for msg in messages

        )