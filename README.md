# GitOps Deployment on EKS
This repository contains the complete solution, demonstrating the design and deployment of a secure, production-ready microservice architecture using Terraform, EKS, and Argo CD driven by GitHub Actions.

---
![System Architecture Diagram](Architectural-design/cloud-challenge.jpeg)

## Architectural Overview
The application is deployed onto a dedicated EKS cluster and consists of a secure two-tier microservice architecture. Both services are configured for Burstable Quality of Service (QoS), ensuring stability and resource efficiency.
### Main API: 
- Public-facing service exposed via an AWS LoadBalancer. It handles request routing, versioning, and provides the interface for application testing.
### Auxiliary Service: 
- Private, internal service responsible solely for secure, credential-less interaction with specific AWS services (S3 and SSM Parameter Store).
### GitOps: 
- Argo CD acts as the single source of truth, managing the cluster state by observing the k8s directory in this repository.

### Resource Efficiency:
- Both services are configured with Burstable QoS for optimal stability and cost efficiency.

---

## Implementation Details

## 1. Security & Infrastructure (IRSA)
Infrastructure is defined using Terraform, focused on security and enablement within the EKS environment.

#### IAM Roles for Service Accounts (IRSA)
- The Auxiliary Service interacts with AWS using IRSA.
- Terraform provisions:
  - IAM Role
  - IAM Policy
  - Kubernetes ServiceAccount binding  
- No static AWS credentials are stored in the application.

#### Principle of Least Privilege
The IAM policy allows only:
- `s3:ListAllMyBuckets`
- `ssm:GetParameter`

#### Testing Resources
Terraform provisions:
- A test S3 bucket  
- An SSM parameter

---

## 2. CI/CD & GitOps Automation

A fully automated closed-loop GitOps workflow is implemented.

#### Closed-Loop Git Write-Back
The GitHub Actions pipeline:
1. Builds container images  
2. Pushes them to the registry  
3. Updates the `k8s/kustomization.yaml` image tags  
4. Commits the changes back to the repository  

This ensures the repository always reflects the deployed cluster state.

#### Argo CD Sync
When a manifest update is pushed:
- Argo CD detects the change
- Pulls the new image tag
- Applies the update to the cluster automatically

---

## 3. Stability and High Availability (HPA & PDB)
The manifests are configured for production readiness, ensuring automatic scaling and protection against maintenance disruptions.

- Horizontal Pod Autoscaler (HPA): HPAs for both services scale the replicas based on CPU utilization, ensuring automatic resilience under varying traffic loads.
- Pod Disruption Budget (PDB): PDBs are configured with `maxUnavailable: 1` for both services, guaranteeing that a quorum of pods remains available during planned cluster maintenance (e.g., node drains), thereby preventing service outages.
- Resource Management: All Deployments include accurate resource requests (for stable scheduling) and limits (to prevent resource contention), enforcing the Burstable QoS class.

## Deployment Instructions
### Prerequisites
EKS Cluster provisioned with OIDC enabled.
Argo CD deployed to the cluster.

### Step 1: 
Create namespaces on the cluster as the next step depends on it (`main-service-ns`, `aux-service-ns`)
### Step 2: Deploy Infrastructure (Terraform Code)
Deploy the required application services and security components (IRSA, S3, SSM) into the existing EKS environment.

cd terraform-scripts/
- `terraform init`
- `terraform plan`
- `terraform apply`

### Step 3: Configure Argo CD Application
Instal and Apply the Argo CD Application manifest to begin cluster synchronization.

#### To install:
- `kubectl create namespace argocd`
- `kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`

#### To apply the Argo CD Application manifest:
Run command from the root directory:
`kubectl apply -f application.yaml -n argocd`

### Step 4: Verify Deployment Success
#### Argo CD Check: 
Confirm the cloud-challenge-app (or your application name) shows Synced and Healthy in the Argo CD UI/CLI.
#### API URL: 
Retrieve the external URL for the LoadBalancer service:

`kubectl get svc main-service-lb -n main-service-ns`

The EXTERNAL-IP is your base URL for testing.

---

## API Usage and Testing Guide
The Main API endpoints are used to verify the secure, credential-less integration with AWS through the IRSA-enabled Auxiliary Service.

### 1. List All S3 Buckets (Verifies IRSA S3 Access)
This confirms the Auxiliary Service's IAM Role has the necessary s3:ListAllMyBuckets permission.
Request:

`curl -X GET http://EXTERNAL-IP/s3/buckets`
#### Expected Response (JSON body):
JSON
{
  "main_api_version": "",
  "aux_service_version": "",
  "data": {
    "buckets": [
    ]
  }
}
### 2. Retrieve SSM Parameter Value (Verifies IRSA SSM Access)
This confirms the Auxiliary Service's IAM Role has the necessary ssm:GetParameter permission.
Request:

`curl -X GET http://EXTERNAL-IP/ssm/parameter/app/database/password`

{
  "main_api_version": "",
  "aux_service_version": "",
  "data": {
    "name": "",
    "value": ""
  }
}

`curl -X GET http://EXTERNAL-IP/ssm/parameter`

#### Expected Response (JSON body):
JSON
{
  "main_api_version": "",
  "aux_service_version": "",
  "data": {
    "parameters": [
      {
        "Name": "",
        "Type": "String",
        "ARN": "arn:aws:ssm:..."
      }
    ]
  }
}
