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
