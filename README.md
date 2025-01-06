# **Minikube Single Node Cluster Deployment**

This project demonstrates the deployment of a Python Flask application to a Kubernetes cluster using Minikube. The application serves a simple API endpoint and scales dynamically based on replica configuration.

---

## **Table of Contents**
1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Steps](#steps)
   - [Install Minikube](#1-install-minikube)
   - [Create the Flask Application](#2-create-the-flask-application)
   - [Create a Docker Image](#3-create-a-docker-image)
   - [Deploy to Minikube](#4-deploy-to-minikube)
   - [Expose the Application](#5-expose-the-application)
   - [Verify the Deployment](#6-verify-the-deployment)
   - [Scale the Deployment](#7-scale-the-deployment)
4. [Outcome](#outcome)
5. [Repository Structure](#repository-structure)
6. [Notes](#notes)

---

## **Overview**

This project involves deploying a Python Flask application to a Kubernetes cluster on Minikube. The application:
- Serves a simple API endpoint at `/lucky-otter-15`.
- Initially runs with **2 replicas**.
- Is exposed via a Kubernetes Service of type `NodePort`.
- Demonstrates scaling by increasing replicas from **2 to 4**.

---

## **Requirements**
- Minikube installed on your local machine.
- Docker installed and configured.
- `kubectl` CLI tool installed.
- A public Docker Hub account for pushing the application image.

---

## **Steps**

### **1. Install Minikube**
- Install Minikube by following the [official documentation](https://minikube.sigs.k8s.io/docs/start/).
- Start the cluster:
  ```bash
  minikube start
  ```

---

### **2. Create the Flask Application**
1. Create a file `app.py` with the following content:
   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route('/lucky-otter-15', methods=['GET'])
   def lucky_otter():
       return {"status": "Application is running"}, 200

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```

2. Create a `requirements.txt` file:
   ```
   Flask==2.0.1
   ```

---

### **3. Create a Docker Image**
1. Write a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "app.py"]
   ```

2. Build and push the Docker image:
   ```bash
   docker build -t <your-dockerhub-username>/flask-app:latest .
   docker push <your-dockerhub-username>/flask-app:latest
   ```

---

### **4. Deploy to Minikube**
1. Create a Kubernetes Deployment in `deployment.yaml`:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: lucky-otter-deployment
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: lucky-otter
     template:
       metadata:
         labels:
           app: lucky-otter
       spec:
         containers:
         - name: flask-app
           image: <your-dockerhub-username>/flask-app:latest
           ports:
           - containerPort: 5000
   ```

2. Apply the Deployment:
   ```bash
   kubectl apply -f deployment.yaml
   ```

---

### **5. Expose the Application**
1. Create a Kubernetes Service in `service.yaml`:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: lucky-otter-service
   spec:
     type: NodePort
     selector:
       app: lucky-otter
     ports:
     - protocol: TCP
       port: 5000
       targetPort: 5000
       nodePort: 30459
   ```

2. Apply the Service:
   ```bash
   kubectl apply -f service.yaml
   ```

---

### **6. Verify the Deployment**
1. Get the Minikube IP:
   ```bash
   minikube ip
   ```

2. Access the API endpoint:
   ```bash
   curl http://<minikube-ip>:30459/lucky-otter-15
   ```
   **Expected response:**
   ```json
   {"status": "Application is running"}
   ```

---

### **7. Scale the Deployment**
1. Scale the Deployment to 4 replicas:
   ```bash
   kubectl scale deployment lucky-otter-deployment --replicas=4
   ```

2. Verify the updated Deployment:
   ```bash
   kubectl get pods
   ```

---

## **Outcome**
- The application is deployed with **2 replicas** and later scaled to **4 replicas**.
- The application is exposed on port `30459` and serves the endpoint `/lucky-otter-15`.

---

## **Repository Structure**
```
.
├── app.py
├── requirements.txt
├── Dockerfile
├── deployment.yaml
├── service.yaml
└── README.md
```

---

## **Notes**
- Replace `<your-dockerhub-username>` with your actual Docker Hub username in the `Dockerfile` and `deployment.yaml`.
- Ensure Minikube is running before deploying the application.

---

Install Minikube: Set up a local Kubernetes cluster.
minikube start

![Screenshot 2025-01-04 142404](https://github.com/user-attachments/assets/348f1b9d-ac6e-495d-abce-64bbb1561274)

![Screenshot 2025-01-04 142349](https://github.com/user-attachments/assets/42baf6c1-c22e-45bf-a06e-b301a1a2c70d)

![image](https://github.com/user-attachments/assets/fa736e64-4668-4be7-ac06-64c1e14b80c4)

![image](https://github.com/user-attachments/assets/5a97d794-19d4-464f-93af-98a102968eaa)

![image](https://github.com/user-attachments/assets/7fd37b2d-438f-4187-862c-cf63319f8604)

![image](https://github.com/user-attachments/assets/15112367-ce8e-4fb9-9d3f-dd54834b2103)

![image](https://github.com/user-attachments/assets/f46a563c-f851-48b9-aa76-6f52362e49f7)

![image](https://github.com/user-attachments/assets/d698a6d4-3432-4ab1-9da6-ec178554f0f2)

![image](https://github.com/user-attachments/assets/a70ba823-c833-47a8-ba77-dfb296effa85)

![image](https://github.com/user-attachments/assets/0a440c86-372b-4678-bf25-afc327234ef9)

![Screenshot 2025-01-04 123705](https://github.com/user-attachments/assets/03911518-4277-435c-912f-e8ba4a18b3be)

![Screenshot 2025-01-04 120824](https://github.com/user-attachments/assets/35128e00-9015-455d-bccd-2c3479997a71)


![Screenshot 2025-01-06 121205](https://github.com/user-attachments/assets/6651d358-adb1-46dc-af29-4e62364d8d1e)

![Screenshot 2025-01-04 125008](https://github.com/user-attachments/assets/6fddeada-5936-4702-b1db-515d26674932)

