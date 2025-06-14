# monitoring.py
from monitoring import init_metrics

from prometheus_flask_exporter import PrometheusMetrics
from flask import request
import time

metrics = None

def init_metrics(app):
    global metrics
    metrics = PrometheusMetrics(app)
    
    # Métriques statiques
    metrics.info('app_info', 'Application info', version='1.0.0')
    
    # Métriques de requêtes
    metrics.register_default(
        metrics.counter(
            'flask_http_request_total', 'Total HTTP Requests',
            labels={'method': lambda: request.method, 'endpoint': lambda: request.endpoint}
        )
    )
    
    # Métriques de latence
    metrics.register_default(
        metrics.histogram(
            'flask_http_request_duration_seconds', 'HTTP Request Duration',
            labels={'method': lambda: request.method, 'endpoint': lambda: request.endpoint}
        )
    )
    
    # Métriques personnalisées pour les fonctionnalités métier
    moto_counter = metrics.counter(
        'moto_views_total', 'Total views of motorcycle details',
        labels={'moto_id': lambda: request.view_args.get('id', 'unknown')}
    )
    
    # Métriques de base de données
    db_query_histogram = metrics.histogram(
        'db_query_duration_seconds', 'Database Query Duration',
        labels={'query_type': lambda: 'unknown'}
    )
    
    # Décorateurs pour fonctions spécifiques
    @app.before_request
    def before_request():
        request.start_time = time.time()
        
    @app.after_request
    def after_request(response):
        # Enregistrement du temps de réponse
        if hasattr(request, 'start_time'):
            request_latency = time.time() - request.start_time
            metrics.histogram('response_latency_seconds', 'Response latency').observe(request_latency)
        return response
    
    # Décorateur pour les métriques sur les détails de moto
    def track_moto_views(route_function):
        def wrapper(*args, **kwargs):
            if 'id' in kwargs:
                moto_counter.labels(moto_id=str(kwargs['id'])).inc()
            return route_function(*args, **kwargs)
        wrapper.__name__ = route_function.__name__
        return wrapper
    
    # Décorateur pour les métriques de base de données
    def track_db_query(query_type):
        def decorator(query_function):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = query_function(*args, **kwargs)
                query_time = time.time() - start_time
                db_query_histogram.labels(query_type=query_type).observe(query_time)
                return result
            return wrapper
        return decorator
    
    return {
        'track_moto_views': track_moto_views,
        'track_db_query': track_db_query
    }
