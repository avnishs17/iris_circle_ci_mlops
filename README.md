# Iris MLOps Pipeline with CircleCI and GKE

This project demonstrates a complete MLOps pipeline for the Iris dataset classification using CircleCI for CI/CD and Google Kubernetes Engine (GKE) for deployment.

## Project Overview

The pipeline includes:
- Data processing and model training
- Docker containerization
- Automated CI/CD with CircleCI
- Artifact storage in Google Artifact Registry
- Deployment to Google Kubernetes Engine

## Prerequisites

- Google Cloud Platform account
- GCP Service account with the following permissions:
  - Artifact Registry Administrator
  - Artifact Registry Writer
  - Owner
  - Storage Object Admin
  - Storage Object Viewer
- CircleCI account

## Setup Instructions

### 1. Google Cloud Platform Setup (via Web Interface)

#### 1.1 Create a GCP Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project" or select project dropdown
3. Enter project name and ID
4. Click "Create"

#### 1.2 Create Artifact Registry Repository
1. Navigate to **Artifact Registry** in the GCP Console
2. Click **"Create Repository"**
3. Set the following:
   - **Name**: `iris`
   - **Format**: Docker
   - **Location**: `us-central1` (or your preferred region)
   - **Description**: "Docker repository for Iris MLOps project"
4. Click **"Create"**

#### 1.3 Create GKE Cluster
1. Navigate to **Kubernetes Engine > Clusters**
2. Click **"Create Cluster"**
3. Choose **"Standard"** cluster
4. Configure cluster:
   - **Name**: `iris-cluster`
   - **Location**: Select **"Regional"** and choose `us-central1`
   - **✅ Enable Cluster DNS** (tick this option)
5. Click **"Create"**

#### 1.4 Create Service Account
1. Navigate to **IAM & Admin > Service Accounts**
2. Click **"Create Service Account"**
3. Set details:
   - **Name**: `circleci-service-account`
   - **Description**: "Service account for CircleCI"
4. Click **"Create and Continue"**
5. Grant the following roles:
   - **Artifact Registry Administrator**
   - **Artifact Registry Writer**
   - **Owner**
   - **Storage Object Admin**
   - **Storage Object Viewer**
6. Click **"Continue"** then **"Done"**

#### 1.5 Download Service Account Key
1. In **Service Accounts**, find your `circleci-service-account`
2. Click on the service account name
3. Go to **"Keys"** tab
4. Click **"Add Key" > "Create new key"**
5. Select **JSON** format
6. Click **"Create"**
7. **Rename the downloaded file to `gcp-key.json`**
8. **Keep this file secure - DO NOT commit to version control**

### 2. CircleCI Setup

#### 2.1 Connect Repository to CircleCI
1. Go to [CircleCI](https://circleci.com/)
2. Sign in with your GitHub/GitLab account
3. Add your project repository

#### 2.2 Configure Environment Variables

In your CircleCI project settings, add the following environment variables:

##### Required Environment Variables:

1. **GCLOUD_SERVICE_KEY**
   ```bash
   # Generate base64 encoded service account key
   cat gcp-key.json | base64 -w 0
   ```
   Copy the entire base64 output and paste it as the value for `GCLOUD_SERVICE_KEY`

2. **GOOGLE_PROJECT_ID**
   ```
   your-project-id
   ```

3. **GKE_CLUSTER**
   ```
   iris-cluster
   ```

4. **GOOGLE_COMPUTE_REGION**
   ```
   us-central1
   ```

#### 2.3 Setting Environment Variables in CircleCI
1. Go to your project in CircleCI
2. Click on "Project Settings"
3. Navigate to "Environment Variables"
4. Click "Add Environment Variable"
5. Add each variable with its corresponding value

### 3. Local Development Setup

#### 3.1 Clone and Setup Project
```bash
git clone <your-repository-url>
cd iris_circle_ci_mlops

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

#### 3.2 Run Training Pipeline Locally
```bash
python pipeline/training_pipeline.py
```

#### 3.3 Run Flask Application Locally
```bash
python app.py
```

### 4. Deployment Process

The deployment is fully automated through CircleCI. When you push changes to your GitHub repository:

1. **CircleCI automatically triggers** the pipeline
2. **Builds Docker image** in the cloud
3. **Pushes to Artifact Registry**
4. **Deploys to GKE cluster**

**No local Docker building required!** CircleCI handles everything automatically.

### 5. CI/CD Pipeline (Fully Automated)

When you push code to your GitHub repository, CircleCI automatically:

1. **Checkout Code**: Retrieves the latest code from the repository
2. **Build Docker Image**: 
   - Authenticates with Google Cloud using service account
   - Builds Docker image from your Dockerfile
   - Pushes image to Artifact Registry (`us-central1-docker.pkg.dev/YOUR_PROJECT/iris/iris:latest`)
3. **Deploy to GKE**:
   - Authenticates with Google Cloud
   - Configures kubectl for your GKE cluster
   - Applies Kubernetes deployment using `kubernetes-deployment.yaml`

**Just push your changes - CircleCI does the rest!**

### 6. Monitoring and Verification

#### 6.1 Check CircleCI Pipeline
- Monitor builds in CircleCI dashboard
- Review logs for any failures

#### 6.2 Access Application
Once CircleCI completes the deployment:
1. Go to **Google Cloud Console > Kubernetes Engine > Services & Ingress**
2. Find the `iris-service`
3. Note the **External IP address**
4. Access the application at `http://<EXTERNAL-IP>:5000`

#### 6.3 Monitor Application (via GCP Console)
- **Kubernetes Engine > Workloads**: Check pod status
- **Kubernetes Engine > Services & Ingress**: View service details
- **Logging**: View application logs

## Project Structure

```
iris_circle_ci_mlops/
├── .circleci/
│   └── config.yml              # CircleCI pipeline configuration
├── artifacts/                  # Model artifacts and processed data
├── pipeline/
│   └── training_pipeline.py    # ML training pipeline
├── src/                        # Source code modules
├── static/                     # Static files for Flask app
├── templates/                  # HTML templates
├── app.py                      # Flask application
├── Dockerfile                  # Docker configuration
├── kubernetes-deployment.yaml  # Kubernetes deployment config
├── requirements.txt           # Python dependencies
└── setup.py                   # Package setup
```

## Security Notes

- Never commit `gcp-key.json` to version control
- Store all sensitive information in CircleCI environment variables
- Use least privilege principle for service account permissions
- Regularly rotate service account keys

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify service account has correct permissions
   - Check if `GCLOUD_SERVICE_KEY` is correctly base64 encoded

2. **Docker Push Failures**
   - Ensure Artifact Registry repository exists
   - Verify repository permissions

3. **GKE Deployment Issues**
   - Check cluster connectivity
   - Verify kubectl configuration
   - Review Kubernetes deployment YAML

4. **Application Not Accessible**
   - Check service external IP assignment
   - Verify firewall rules
   - Check pod logs for errors