# monitoring.py

from prometheus_flask_exporter import PrometheusMetrics

# Singleton pattern to avoid double registration
metrics = None

def setup_metrics(app):
    global metrics
    if metrics is not None:
        return metrics  # Already initialized, avoid duplicate

    # Initialize PrometheusMetrics
    metrics = PrometheusMetrics(app)

    # Add custom metrics if needed
    # Example: custom counter (different name to avoid collision with default)
    from prometheus_client import Counter

    custom_counter = Counter(
        'custom_http_request_total',  # Make sure name is unique
        'Total custom HTTP Requests',
        ['method', 'endpoint']
    )

    # Record requests (Flask signal hook)
    @app.before_request
    def before_request():
        if metrics.app:
            custom_counter.labels(
                method=getattr(app.request, 'method', 'unknown'),
                endpoint=getattr(app.request, 'endpoint', 'unknown')
            ).inc()

    return metrics
