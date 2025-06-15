# app/monitoring.py

from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
from flask import request

# Singleton global to avoid double registration
metrics = None
custom_counter = None

def setup_metrics(app):
    global metrics, custom_counter

    if metrics is not None:
        return metrics  # Already initialized, avoid duplicate

    # Initialize PrometheusMetrics
    metrics = PrometheusMetrics(app)

    # Custom metric with unique name
    custom_counter = Counter(
        'custom_http_request_total',
        'Total custom HTTP Requests',
        ['method', 'endpoint']
    )

    # Track request method and endpoint
    @app.before_request
    def before_request():
        if request.endpoint:
            custom_counter.labels(
                method=request.method,
                endpoint=request.endpoint
            ).inc()

    return metrics
