# 🛡️ **LLMOps Cybersecurity Analyzer — Main Project Overview**

The **LLMOps Cybersecurity Analyzer** is a complete end-to-end system that performs **AI-assisted security analysis** on Python code using:

* **OpenAI Agents + MCP servers**
* **Semgrep static analysis integration**
* A **React/Next.js frontend**
* A **FastAPI backend**
* Full **Google Cloud Run deployment** using Terraform
* Automated container builds through Docker

The goal of this project is to deliver a production-grade, cloud-deployable LLMOps workflow for performing static + AI security analysis with consistent, repeatable infrastructure.

## 🎥 **Cybersecurity Analyzer Demo**

<div align="center">
  <img src="assets/app/cyber_analyzer.gif" width="100%" alt="Cybersecurity Analyzer Demo">
</div>

This is the deployed version of the application, running in Google Cloud Run.

## 🧩 **Grouped Stages**

This GCP version of the project consists of **two core stages**, covering setup and deployment.

|  Stage | Category         | Description                                                                                |
| :----: | ---------------- | ------------------------------------------------------------------------------------------ |
| **00** | GCP Setup        | Creating a GCP account, enabling billing, setting budget alerts, installing the gcloud CLI |
| **01** | Cloud Run Deploy | Terraform-based deployment to Cloud Run and Container Registry                             |

This provides a clean lifecycle:
**prepare GCP → deploy to Cloud Run**

## 🗂️ **Project Structure**

```
LLMOps-Cybersecurity-Analyzer/
├── assets/
│   ├── app/
│   │   └── cyber_analyzer.gif
│   └── gcp/
│       └── new_project.png
├── backend/
│   ├── context.py
│   ├── mcp_servers.py
│   ├── pyproject.toml
│   ├── server.py
│   ├── uv.lock
│   ├── .python-version
│   ├── .venv/
│   └── __pycache__/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── app/
│   │   └── components/
│   │       ├── AnalysisResults.tsx
│   │       ├── CodeInput.tsx
│   │       ├── FileUpload.tsx
│   │       └── README.md
│   │   └── types/
│   ├── .next/
│   ├── node_modules/
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.ts
│   ├── eslint.config.mjs
│   ├── postcss.config.mjs
│   └── tsconfig.json
├── terraform/
│   ├── azure/          # Legacy folder (not used in GCP version)
│   └── gcp/
│       ├── main.tf
│       ├── variables.tf
│       └── allow-all-policy.yaml
├── airline.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env
└── README.md
```

## 🧠 **Core Components of the System**

### 🔎 FastAPI Backend (Python)

The backend handles:

* AI-driven semantic analysis using OpenAI Agents
* One-shot Semgrep scanning through the MCP server
* Merging LLM findings + static analysis
* Structured, validated vulnerability reporting

### 🖥️ Next.js Frontend (React)

The frontend provides:

* File upload
* Display of vulnerabilities in table form
* Code snippets and recommended fixes
* Summary and explanation generation
* Clean UI with fast local Dev experience

### 🛠️ MCP + Semgrep

The MCP server integrates Semgrep in a safe, controlled environment:

* Executes a single scan per request
* Ensures rule safety
* Passes structured Semgrep output back to the backend
* Provides deep static analysis to augment LLM reasoning

### ☁️ Google Cloud Infrastructure (Terraform)

Terraform provisions:

* Google Container Registry
* Cloud Build (for image building)
* Cloud Run (serverless container hosting)
* Public access IAM policies
* Required Cloud APIs

This results in a **fast, scalable, low-maintenance deployment environment** with automatic HTTPS and per-request billing.

## 💻 **Local Development**

### Backend

```bash
cd backend
uv run server.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Local Docker Test

```bash
docker build -t cyber-analyzer .
docker run --rm -p 8000:8000 --env-file .env cyber-analyzer
```

## 🚀 **Cloud Run Deployment (Stage 01)**

### Deployment

```bash
cd terraform/gcp

terraform init
terraform workspace new gcp
terraform apply \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

### Retrieve your service URL

```bash
terraform output service_url
```

### Destroy when finished

```bash
terraform destroy \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

## **Summary**

The **LLMOps Cybersecurity Analyzer (GCP Edition)** provides a complete production-ready security analysis pipeline using:

* OpenAI Agents
* Semgrep MCP server
* Dockerized FastAPI backend
* Next.js frontend
* Fully automated Terraform deployment to Cloud Run

This project demonstrates a professional LLMOps workflow:
**local development → MCP static analysis → GCP infrastructure → Cloud Run deployment**
