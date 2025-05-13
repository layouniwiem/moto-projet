#!/bin/bash

# Set the namespace variable
NAMESPACE="moto-app"

echo "1. Verifying namespace exists..."
kubectl get namespace $NAMESPACE || kubectl create namespace $NAMESPACE

echo "2. Setting up port forwarding (if not already running)..."
# Kill any existing port forwarding on port 8080
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
# Start new port forwarding in the background
kubectl port-forward -n $NAMESPACE svc/flask-app 8080:5000 &

echo "3. Applying corrected ingress configuration..."
# Apply the fixed ingress configuration
kubectl apply -f fixed-ingress.yaml -n $NAMESPACE

echo "4. Checking ingress status..."
kubectl get ingress -n $NAMESPACE

echo "5. Checking pod status..."
kubectl get pods -n $NAMESPACE

echo "6. Verifying ingress controller is running..."
kubectl get pods -n ingress-nginx || kubectl get pods -A | grep ingress

echo "7. Testing connection locally..."
curl -v http://localhost:8080

echo "8. Testing connection via domain name..."
curl -v http://moto-app.example.com

echo "Done! If issues persist, run 'kubectl describe ingress moto-app-ingress -n $NAMESPACE' for more details."