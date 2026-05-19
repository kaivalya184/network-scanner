from flask import Flask, render_template, jsonify

from scanner import (
    scan_network,
    get_local_ip,
    get_network_range,
    get_ipv6_addresses
)

import threading
from datetime import datetime

app = Flask(__name__)

scan_results = []

scan_status = {
    "running": False,
    "done": False,
    "last_scan": None
}

# =========================================
# HOME
# =========================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )

# =========================================
# START SCAN
# =========================================

@app.route("/start-scan", methods=["POST"])
def start_scan():

    global scan_results
    global scan_status

    if scan_status["running"]:

        return jsonify({
            "message": "Scan already running"
        }), 400

    scan_results = []

    scan_status = {
        "running": True,
        "done": False,
        "last_scan": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    def run():

        global scan_results
        global scan_status

        try:

            scan_results = scan_network()

        except Exception as e:

            print("Scan Error:", e)

        scan_status["running"] = False
        scan_status["done"] = True

    threading.Thread(
        target=run,
        daemon=True
    ).start()

    return jsonify({
        "message": "Scan started"
    })

# =========================================
# RESULTS
# =========================================

@app.route("/results")
def results():

    ipv6 = get_ipv6_addresses()

    return jsonify({

        "status": scan_status,

        "results": scan_results,

        "local_ip": get_local_ip(),

        "network_range": get_network_range(
            get_local_ip()
        ),

        "ipv6_addresses": ipv6,

        "device_count": len(scan_results)
    })

# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )