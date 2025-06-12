Voici une **documentation complète** pour déployer le projet *"Application Web de Vente de Motos"* avec **Kubernetes, Ansible, Docker et Jenkins**, basée sur les deux documents fournis.

---

#  Documentation de Déploiement du Projet Moto-App

##  1. Prérequis

*  Docker / Docker Compose
*  Kubernetes (Minikube ou K3s)
*  Ansible (2.10+)
*  Jenkins (pour CI/CD)
*  Accès à DockerHub (ex. : `layouniwiem/devops_riders`)
*  Accès sudo sur les machines distantes (via SSH)

---

##  2. Structure Technique

* **Backend** : Flask (Python)
* **Base de données** : MariaDB
* **Déploiement** :

  * Kubernetes (manifestes K8s)
  * Docker (image containerisée)
  * Ansible (automatisation)
  * Jenkins (CI/CD)
  * Monitoring (Prometheus, Grafana)

---

##  3. Déploiement Manuel Kubernetes (via scripts)

### Étapes :

1. **Construire l’image Docker :**

```bash
cd app
docker build -t my-flask-app .
docker tag my-flask-app layouniwiem/devops_riders:latest
docker push layouniwiem/devops_riders:latest
```

2. **Appliquer les manifestes Kubernetes :**

```bash
kubectl create namespace moto-app
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/config-map.yaml
kubectl apply -f k8s/persistent-volumes.yaml
kubectl apply -f k8s/db-init-configmap.yaml
kubectl apply -f k8s/mariadb-deployment.yaml
kubectl apply -f k8s/mariadb-service.yaml
kubectl apply -f k8s/flask-deployment.yaml
kubectl apply -f k8s/flask-service.yaml
kubectl apply -f k8s/ingress.yaml
```

3. **Tester localement l’application :**

```bash
kubectl port-forward svc/flask-app 8080:5000 -n moto-app
curl http://localhost:8080
```

---

##  4. Déploiement Automatisé avec Ansible

###  Rôles disponibles :

* `roles/docker`
* `roles/database`
* `roles/app`
* `roles/jenkins`
* `roles/kubernetes`
* `roles/monitoring`

###  Exemple de Playbook :

```yaml
- name: Setup complet
  hosts: all
  become: true
  roles:
    - docker
    - database
    - app
    - kubernetes
    - jenkins
    - monitoring
```

Fichiers d’inventaire : `inventory.ini` / `inventory.yml`
Variables comme `mariadb_user`, `app_repo_url`, etc., sont définies dans les `group_vars` ou dans les fichiers `vars/*.yml`.

---

##  5. Intégration Continue (CI/CD) avec Jenkins

* Jenkins est déployé via Ansible (`roles/jenkins`)
* L’image de l’application est buildée puis pushée vers Docker Hub
* Déclenchement du pipeline :

  * Build Docker
  * Push vers Docker Hub
  * Déploiement sur cluster via `kubectl`

---

##  6. Monitoring

### Outils utilisés :

* **Prometheus** pour la collecte des métriques
* **Node Exporter** pour les métriques machines
* **Grafana** pour les dashboards

### Déploiement :

```yaml
- name: Monitoring
  hosts: localhost
  become: true
  roles:
    - monitoring
```

---

##  7. Tests et Validation

Un test unitaire de la route d'accueil est disponible dans `tests/test_home.py` :

```python
def test_homepage():
    app = create_app()
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Motos" in response.data
```

---

##  8. Accès à l'application

* Frontend : `http://localhost:8080` ou `http://moto-app.example.com` via ingress
* Base de données : via `kubectl exec` ou `docker exec` si local

---

##  Commandes Utiles

```bash
# Lister les pods
kubectl get pods -n moto-app

# Vérifier l'état du déploiement
kubectl rollout status deployment/flask-app -n moto-app

# Voir les logs
kubectl logs -l app=flask-app -n moto-app

# Tester l'accès via ingress
curl http://moto-app.example.com
```

---

##  Utilisateurs de Test

```txt
Admin :
  - utilisateur : admin
  - mot de passe : admin123

Utilisateur :
  - utilisateur : user1
  - mot de passe : user123
```

---

Souhaitez-vous que je génère cette documentation au format PDF ou Markdown téléchargeable ?
