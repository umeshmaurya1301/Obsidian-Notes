
 # 1. login to server
	 ssh -i ~/keys/gcpkeys/gcp_key umesh.maurya@34.131.16.43

# 2. Shell Script for setting up Kind
		```bash
			#!/bin/bash

	set -e  # Exit immediately if a command exits with a non-zero status
	set -o pipefail

	echo "🚀 Starting installation of Docker, Kind, and kubectl..."

	# ----------------------------
	# 1. Install Docker
	# ----------------------------
	if ! command -v docker &>/dev/null; then
	  echo "📦 Installing Docker..."
	  sudo apt-get update -y
	  sudo apt-get install -y docker.io

	  echo "👤 Adding current user to docker group..."
	  sudo usermod -aG docker "$USER"

	  echo "✅ Docker installed and user added to docker group."
	else
	  echo "✅ Docker is already installed."
	fi

	# ----------------------------
	# 2. Install Kind (based on architecture)
	# ----------------------------
	if ! command -v kind &>/dev/null; then
	  echo "📦 Installing Kind..."

	  ARCH=$(uname -m)
	  if [ "$ARCH" = "x86_64" ]; then
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.29.0/kind-linux-amd64
	  elif [ "$ARCH" = "aarch64" ]; then
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.29.0/kind-linux-arm64
	  else
    echo "❌ Unsupported architecture: $ARCH"
    exit 1
	  fi

	  chmod +x ./kind
	  sudo mv ./kind /usr/local/bin/kind
	  echo "✅ Kind installed successfully."
	else
	  echo "✅ Kind is already installed."
	fi

	# ----------------------------
	# 3. Install kubectl (latest stable)
	# ----------------------------
	if ! command -v kubectl &>/dev/null; then
	  echo "📦 Installing kubectl (latest stable version)..."

	  curl -LO "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
	  sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
	  rm -f kubectl

	  echo "✅ kubectl installed successfully."
	else
	  echo "✅ kubectl is already installed."
	fi

	# ----------------------------
	# 4. Confirm Versions
	# ----------------------------
	echo
	echo "🔍 Installed Versions:"
	docker --version
	kind --version
	kubectl version --client --output=yaml

	echo
	echo "🎉 Docker, Kind, and kubectl installation complete!"
		```





sudo apt-get update


sudo apt-get install docker.io
sudo usermod -aGdocker $USER && newgrp docker

# create kind cluster config file config.yaml
	```yaml
		kind: Cluster
		apiVersion: kind.x-k8s.io/v1alpha4
		nodes:
		  - role: control-plane
		  - role: worker
		    extraPortMappings:
		      - containerPort: 80
		        hostPort: 8080
		        protocol: TCP
		      - containerPort: 443
		        hostPort: 8443
		        protocol: TCP

	
	```


kind create cluster --name tws-cluster  --config config.yaml

kubectl cluster-info --context kind-tws-cluster

kubectl get nodes