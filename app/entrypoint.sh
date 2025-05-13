#!/bin/bash
# entrypoint.sh
set -e

# Attendre que la base de données soit prête
echo "En attente de la base de données MariaDB..."
until MYSQL_PWD=$MYSQL_PASSWORD mysql -h mariadb -u "$MYSQL_USER" -e "SELECT 1"; do
  echo "MariaDB n'est pas encore disponible - attente..."
  sleep 2
done
echo "MariaDB est prêt!"

# Exécuter la migration de base de données si nécessaire (à implémenter avec Flask-Migrate)
# flask db upgrade

# Démarrer l'application
exec "$@"

# run.py (mise à jour pour inclure le monitoring)
from app import create_app
from app.monitoring import init_metrics

app = create_app()
metrics_tools = init_metrics(app)

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