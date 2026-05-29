from flask import Flask, render_template, jsonify
import psutil
import socket
import getpass
import time
import logging
import os

app = Flask(__name__)

# ---------------------------
# Logging Configuration
# ---------------------------

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# Disable Flask request spam
logging.getLogger("werkzeug").disabled = True

# Dedicated application logger
logger = logging.getLogger("YMLAS")
logger.setLevel(logging.INFO)

logger.info("YMLAS Application Started")


# ---------------------------
# Dashboard Pages
# ---------------------------

@app.route("/")
@app.route("/dashboard")
def dashboard():

    logger.info("Dashboard accessed")

    return render_template("dashboard.html")


@app.route("/logs")
def logs_page():

    logger.info("Logs page opened")

    return render_template("logs.html")


@app.route("/alerts")
def alerts_page():

    logger.info("Alerts page opened")

    return render_template("alerts.html")


@app.route("/deployments")
def deployments_page():

    logger.info("Deployments page opened")

    return render_template("deployments.html")


@app.route("/servers")
def servers_page():

    logger.info("Servers page opened")

    return render_template("servers.html")


@app.route("/settings")
def settings_page():

    logger.info("Settings page opened")

    return render_template("settings.html")


# ---------------------------
# Health Check
# ---------------------------

@app.route("/health")
def health():

    logger.info("Health check requested")

    return jsonify({
        "status": "healthy",
        "service": "YMLAS"
    })


# ---------------------------
# System Metrics API
# ---------------------------

monitor_logger = logging.getLogger("Monitoring")

@app.route("/api/system")
def system_metrics():

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    uptime_hours = uptime_seconds // 3600
    uptime_minutes = (uptime_seconds % 3600) // 60

    # Log only important events

    if cpu > 80:

        monitor_logger.warning(
            f"CPU usage exceeded threshold ({cpu}%)"
        )

    if memory > 80:

        monitor_logger.warning(
            f"Memory usage exceeded threshold ({memory}%)"
        )

    if disk > 85:

        monitor_logger.error(
            f"Disk usage exceeded threshold ({disk}%)"
        )

    return jsonify({

        "hostname": socket.gethostname(),

        "user": getpass.getuser(),

        "cpu": cpu,

        "memory": memory,

        "disk": disk,

        "uptime": f"{uptime_hours}h {uptime_minutes}m"

    })

logger = logging.getLogger("YMLAS")
logger.setLevel(logging.INFO)

monitor_logger = logging.getLogger("Monitoring")
alert_logger = logging.getLogger("Alerts")
deploy_logger = logging.getLogger("Deployments")
server_logger = logging.getLogger("Servers")


# ---------------------------
# Alerts API
# ---------------------------

@app.route("/api/alerts")
def alerts():

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    alert_list = []

    if cpu > 80:

        alert_list.append({

            "severity": "WARNING",

            "message": f"CPU usage high ({cpu}%)"

        })

    if memory > 80:

        alert_list.append({

            "severity": "WARNING",

            "message": f"Memory usage high ({memory}%)"

        })

    if disk > 85:

        alert_list.append({

            "severity": "WARNING",

            "message": f"Disk usage high ({disk}%)"

        })

    if not alert_list:

        alert_list.append({

            "severity": "INFO",

            "message": "All systems operating normally"

        })

    return jsonify(alert_list)


# ---------------------------
# Logs API
# ---------------------------

@app.route("/api/logs")
def logs():

    log_entries = []

    try:

        with open("logs/app.log", "r") as file:

            for line in file:

                parts = line.strip().split("|")

                if len(parts) == 4:

                    log_entries.append({

                        "timestamp": parts[0].strip(),

                        "level": parts[1].strip(),

                        "service": parts[2].strip(),

                        "message": parts[3].strip()

                    })

    except Exception as e:

        logger.error(
            f"Failed reading logs: {str(e)}"
        )

        return jsonify({
            "error": str(e)
        }), 500

    return jsonify(log_entries[::-1])


# ---------------------------
# Deployment History API
# ---------------------------

@app.route("/api/deployments")
def deployments():

    deployment_history = [

        {
            "version": "v1.0.0",
            "status": "Success"
        },

        {
            "version": "v0.9.0",
            "status": "Success"
        },

        {
            "version": "v0.8.0",
            "status": "Failed"
        }

    ]

    return jsonify(deployment_history)


# ---------------------------
# Application Entry Point
# ---------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )