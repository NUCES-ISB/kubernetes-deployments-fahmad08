[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/97WR5HaV)

# 🚀 Flask + PostgreSQL on Kubernetes (Minikube)

This repository contains a **Flask web application** deployed on a **Kubernetes cluster** using **Minikube**. The app connects to a **PostgreSQL database** and allows users to add and retrieve data.

---

## **1️⃣ Start Minikube**
Before deploying, ensure Minikube is running:

```sh
minikube start --driver=docker
```

Verify Minikube status:

```sh
minikube status
```

---

## **2️⃣ Build the Flask App Docker Image**
Minikube runs its own Docker environment. Build the Flask app image inside Minikube:

```sh
eval $(minikube docker-env)  # Use Minikube's Docker
docker build -t flask-app:latest k8s-flask-app/app/
```

---

## **3️⃣ Apply Kubernetes Configurations**
Apply all Kubernetes YAML files to set up PostgreSQL and Flask:

```sh
kubectl apply -f k8s-flask-app/manifests/configmap/postgres-configmap.yaml
kubectl apply -f k8s-flask-app/manifests/secret/postgres-secret.yaml
kubectl apply -f k8s-flask-app/manifests/deployment/postgres-pvc.yaml
kubectl apply -f k8s-flask-app/manifests/deployment/postgres-deployment.yaml
kubectl apply -f k8s-flask-app/manifests/service/postgres-service.yaml
kubectl apply -f k8s-flask-app/manifests/deployment/flask-deployment.yaml
kubectl apply -f k8s-flask-app/manifests/service/flask-service.yaml
```

---



## **4️⃣ Get Flask Service URL**
Expose the Flask service and get its URL:

```sh
minikube service flask-service --url
```

Example output:

```sh
http://192.168.49.2:32145
```

Replace `<minikube-url>` in the steps below with your actual URL.

---

## **5️⃣ Initialize the Database**
Create the users table in PostgreSQL:

```sh
curl <minikube-url>/init
```

Expected Output:

```sh
Table Created!
```

---

## **6️⃣ Add a User**
Send a POST request to add a user:

```sh
curl -X POST <minikube-url>/add \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe"}'
```

Expected Output:

```json
{"id":1,"name":"John Doe"}
```

---

## **7️⃣ Retrieve All Users**
Fetch all users stored in PostgreSQL:

```sh
curl <minikube-url>/users
```

Expected Output:

```json
[{"id":1,"name":"John Doe"}]
```

