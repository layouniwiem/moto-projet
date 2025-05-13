#!/bin/bash

set -e

# 🔧 Configure le bon fichier de configuration Kubernetes
export KUBECONFIG=$HOME/.kube/config


# Chemin absolu du dossier racine du projet, basé sur l'emplacement du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# Transformation en chemin Windows
#PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
windows_path=$(echo "$SCRIPT_DIR" | sed -E 's|/mnt/([a-z])/|\U\1:/|' | sed 's|/|\\|g')

echo "win:$windows_path"
#SCRIPT_DIR="/c/wiem/FilsRouge/moto-project/scripts"
PROJECT_DIR="$(cd "$windows_path\.." && pwd)"  # monte d’un niveau pour atteindre moto-project
DOCKERFILE_DIR="$PROJECT_DIR/app"
DOCKERFILE="$DOCKERFILE_DIR/Dockerfile"



# 🔖 Variables
APP_NAME="my-flask-app"
DOCKER_IMAGE="layouniwiem/devops_riders:latest"
NAMESPACE="moto-app"

# ✅ Vérifier si le Dockerfile existe
if [ ! -f "$DOCKERFILE" ]; then
  echo "❌ Erreur : Le Dockerfile n'a pas été trouvé dans $DOCKERFILE"
  exit 1
fi

# 🚀 Étape 1: Build de l'image Docker
echo "🚀 Étape 1: Build de l'image Docker"
docker build -f "$DOCKERFILE" -t "$APP_NAME" "$DOCKERFILE_DIR"

# 🏷️ Étape 2: Tag et Push de l'image vers Docker Hub
echo "🏷️ Étape 2: Tag et Push de l'image vers Docker Hub"
docker tag "$APP_NAME" "$DOCKER_IMAGE"
docker push "$DOCKER_IMAGE"

# 🧼 Étape 3: Rendre executable entrypoint.sh
echo "🧼 Étape 3: Permission pour entrypoint.sh"
chmod +x "$DOCKERFILE_DIR/entrypoint.sh"

# 🧪 Étape 4: Namespace
echo "🧪 Étape 4: Vérification du namespace"
kubectl get namespace "$NAMESPACE" >/dev/null 2>&1 || kubectl apply -f "$PROJECT_DIR/k8s/namespace.yml"

# 🗂️ Étape 5: Déploiement Kubernetes
echo "🗂️ Étape 5: Déploiement Kubernetes"
kubectl apply -f "$PROJECT_DIR/k8s/config-map.yaml" -n "$NAMESPACE"
kubectl apply -f "$PROJECT_DIR/k8s/secrets.yaml" -n "$NAMESPACE"
kubectl apply -f "$PROJECT_DIR/k8s/persistent-volumes.yaml" -n "$NAMESPACE"
kubectl apply -f "$PROJECT_DIR/k8s/db-init-configmap.yaml" -n "$NAMESPACE"
kubectl apply -f "$PROJECT_DIR/k8s/mariadb-deployment.yaml" -n "$NAMESPACE"
kubectl apply -f "$PROJECT_DIR/k8s/mariadb-service.yaml" -n "$NAMESPACE"
kubectl apply -f "$PROJECT_DIR/k8s/flask-deployment.yaml" -n "$NAMESPACE"
kubectl apply -f "$PROJECT_DIR/k8s/flask-service.yaml" -n "$NAMESPACE"

# 🌐 Étape 6: Activer Ingress
echo "🌐 Étape 6: Activation Ingress"
minikube addons enable ingress || true
kubectl apply -f "$PROJECT_DIR/k8s/ingress.yaml" -n "$NAMESPACE"

# ⏳ Étape 7: Attente pods prêts
echo "🔁 Étape 7: Attente readiness des pods"
kubectl wait --for=condition=Available --timeout=180s deployment/flask-app -n "$NAMESPACE"
kubectl wait --for=condition=Available --timeout=180s deployment/mariadb -n "$NAMESPACE"

# 📊 Étape 8: Résumé
echo "🔎 Étape 8: Services et pods"
kubectl get svc -n "$NAMESPACE"
kubectl get pods -n "$NAMESPACE"

# 🌍 Étape 9: IP Minikube
echo "🌍 Étape 9: IP Minikube"
minikube ip

echo "✅ 📦 Déploiement terminé avec succès !"
