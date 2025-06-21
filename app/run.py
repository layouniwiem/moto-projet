
# run.py (mise à jour pour inclure le monitoring)
from app import create_app
from monitoring import setup_metrics  # Assurez-vous du bon chemin


app = create_app()
setup_metrics(app) 


# Ajouter les décorateurs de métriques aux routes
from app.routes import main, auth

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
@app.route('/health')
def health_check():
    """Health check endpoint for Kubernetes probes"""
    try:
        # Check if database connection is working
        db_status = check_database_connection()
        
        if db_status:
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'timestamp': datetime.utcnow().isoformat()
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected',
                'timestamp': datetime.utcnow().isoformat()
            }), 503
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503

def check_database_connection():
    """Check if database connection is working"""
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST', 'mariadb.moto-app.svc.cluster.local'),
            user=os.environ.get('MYSQL_USER', 'moto_user'),
            password=os.environ.get('MYSQL_PASSWORD', 'moto_password'),
            database=os.environ.get('MYSQL_DATABASE', 'moto_db'),
            connection_timeout=5
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            connection.close()
            return True
        return False
        
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False

# Simple health check without database dependency (for initial startup)
@app.route('/ready')
def readiness_check():
    """Simple readiness check without external dependencies"""
    return jsonify({
        'status': 'ready',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)