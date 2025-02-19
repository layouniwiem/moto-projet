# Application Web de Vente de Motos

## Description
Application web développée avec Flask permettant de visualiser et gérer des annonces de motos d'occasion. L'application inclut une authentification utilisateur et une interface responsive pour afficher les détails des motos.

## Fonctionnalités
- 📱 Interface responsive
- 🔐 Système d'authentification
- 📋 Liste des motos disponibles
- 🔍 Page de détails pour chaque moto
- 💾 Stockage des données dans MariaDB

## Prérequis
- Docker Desktop
- Docker Compose
- Git (optionnel)

## Structure du Projet
```
moto-project/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   └── config.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   └── moto_details.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
├── docker-compose.yml
├── Dockerfile.web
├── init.sql
└── requirements.txt
```

## Installation

### 1. Cloner le projet (optionnel)
```bash
git clone <url-du-projet>
cd moto-project
```

### 2. Lancer l'application avec Docker
```bash
# Construire et démarrer les conteneurs
docker-compose up --build

# Pour lancer en arrière-plan
docker-compose up -d --build
```

### 3. Accéder à l'application
- Interface web : http://localhost:5000
- Base de données : localhost:3306

## Utilisation

### Comptes de test
```
Admin:
- Utilisateur: admin
- Mot de passe: admin123

Utilisateur:
- Utilisateur: user1
- Mot de passe: user123
```

### Commandes Docker utiles
```bash
# Arrêter l'application
docker-compose down

# Voir les logs
docker-compose logs -f

# Redémarrer un service
docker-compose restart web

# Accéder au shell du conteneur web
docker-compose exec web bash

# Accéder à la base de données
docker-compose exec db mysql -u moto_user -p moto_db
```

## Configuration

### Variables d'environnement
L'application utilise les variables d'environnement suivantes :
```
DATABASE_URL=mysql+pymysql://moto_user:moto_password@db/moto_db
FLASK_APP=app
FLASK_ENV=development
```

### Base de données
La base de données est automatiquement initialisée avec :
- Tables nécessaires
- Utilisateurs de test
- Quelques motos d'exemple

## Développement

### Structure de la base de données
```sql
User:
- id (INT, PRIMARY KEY)
- username (VARCHAR(64))
- email (VARCHAR(120))
- password_hash (VARCHAR(128))

Moto:
- id (INT, PRIMARY KEY)
- marque (VARCHAR(50))
- modele (VARCHAR(50))
- annee (INT)
- kilometrage (INT)
- prix (FLOAT)
- description (TEXT)
- date_ajout (DATETIME)
- image_url (VARCHAR(200))
```

### Ajouter une nouvelle moto
```sql
INSERT INTO moto (marque, modele, annee, kilometrage, prix, description)
VALUES ('Marque', 'Modèle', 2023, 1000, 10000, 'Description');
```

## Sécurité
- Authentification requise pour certaines actions
- Mots de passe hashés avec Werkzeug
- Protection CSRF active
- Sessions sécurisées

## Dépannage

### Problèmes courants

1. Docker ne démarre pas
```bash
# Vérifier le statut de Docker
docker --version
docker-compose --version
```

2. Base de données inaccessible
```bash
# Vérifier les logs de la base de données
docker-compose logs db
```

3. Application web inaccessible
```bash
# Vérifier les logs de l'application
docker-compose logs web
```

## Support

Pour tout problème ou question :
1. Vérifier les logs Docker
2. Consulter la documentation
3. Contacter l'équipe de développement

## License
MIT License
