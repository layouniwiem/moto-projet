# monitoring.py
#from monitoring import init_metrics

from prometheus_flask_exporter import PrometheusMetrics
from flask import request
import time

metrics = None

def init_metrics(app):
    global metrics
    metrics = PrometheusMetrics(app)
    
    # Static info metric
    metrics.info('app_info', 'Application info', version='1.0.0')
    
    # HTTP request count
    http_request_counter = metrics.counter(
        'flask_http_request_total', 'Total HTTP Requests',
        labels={'method': lambda: request.method, 'endpoint': lambda: request.endpoint}
    )
    
    # HTTP request duration histogram
    http_request_histogram = metrics.histogram(
        'flask_http_request_duration_seconds', 'HTTP Request Duration',
        labels={'method': lambda: request.method, 'endpoint': lambda: request.endpoint}
    )
    
    # Response latency histogram
    response_latency_histogram = metrics.histogram(
        'response_latency_seconds', 'Response latency',
        labels={'method': lambda: request.method, 'endpoint': lambda: request.endpoint}
    )
    
    # Moto views counter (custom metric)
    moto_counter = metrics.counter(
        'moto_views_total', 'Total views of motorcycle details',
        labels={'moto_id': lambda: request.view_args.get('id', 'unknown')}
    )
    
    # DB query duration histogram
    db_query_histogram = metrics.histogram(
        'db_query_duration_seconds', 'Database Query Duration',
        labels={'query_type': lambda: 'unknown'}
    )
    
    @app.before_request
    def before_request():
        request.start_time = time.time()
        http_request_counter.inc()
    
    @app.after_request
    def after_request(response):
        if hasattr(request, 'start_time'):
            latency = time.time() - request.start_time
            http_request_histogram.observe(latency)
            response_latency_histogram.observe(latency)
        return response
    
    def track_moto_views(route_function):
        @wraps(route_function)
        def wrapper(*args, **kwargs):
            if 'id' in kwargs:
                moto_counter.labels(moto_id=str(kwargs['id'])).inc()
            return route_function(*args, **kwargs)
        return wrapper
    
    def track_db_query(query_type):
        def decorator(query_function):
            @wraps(query_function)
            def wrapper(*args, **kwargs):
                start = time.time()
                result = query_function(*args, **kwargs)
                duration = time.time() - start
                db_query_histogram.labels(query_type=query_type).observe(duration)
                return result
            return wrapper
        return decorator
    
    return {
        'track_moto_views': track_moto_views,
        'track_db_query': track_db_query
    }