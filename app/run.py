
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)