#!/bin/bash

set -e

APP_NAME="my-flask-app"
DOCKER_IMAGE="layouniwiem/devops_riders:latest"
NAMESPACE="moto-app"

echo "🚀 Étape 1: Build de l'image Docker"
docker build -f Dockerfile.web -t $APP_NAME .

echo "🏷️ Étape 2: Tag et Push de l'image vers Docker Hub"
docker tag $APP_NAME $DOCKER_IMAGE
docker push $DOCKER_IMAGE

echo "🧼 Étape 3: Conversion et permission de entrypoint.sh"
dos2unix app/entrypoint.sh
chmod +x app/entrypoint.sh

echo "🧪 Étape 4: Vérification et création du namespace"
kubectl get namespace $NAMESPACE || kubectl apply -f k8s/namespace.yml

echo "🗂️ Étape 5: Déploiement des ressources Kubernetes"

kubectl apply -f k8s/config-map.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/persistent-volumes.yaml
kubectl apply -f k8s/db-init-configmap.yaml

kubectl apply -f k8s/mariadb-deployment.yaml
kubectl apply -f k8s/mariadb-service.yaml

kubectl apply -f k8s/flask-deployment.yaml
kubectl apply -f k8s/flask-service.yaml

echo "🌐 Étape 6: Activation d'Ingress (si non activé)"
minikube addons enable ingress || true
kubectl apply -f k8s/ingress.yaml

echo "🔁 Étape 7: Patience... Attente que les pods soient prêts"
kubectl wait --for=condition=Available --timeout=180s deployment/flask-app -n $NAMESPACE
kubectl wait --for=condition=Available --timeout=180s deployment/mariadb -n $NAMESPACE

echo "🔎 Étape 8: Résumé des services déployés"
kubectl get svc -n $NAMESPACE
kubectl get pods -n $NAMESPACE

echo "🌍 Étape 9: IP Minikube pour accès web"
minikube ip

echo "📦 Déploiement terminé avec succès !"
