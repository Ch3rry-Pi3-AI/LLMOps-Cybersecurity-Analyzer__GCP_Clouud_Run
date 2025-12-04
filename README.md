# 🛡️ **LLMOps Cybersecurity Analyzer — Main Project Overview**

The **LLMOps Cybersecurity Analyzer** is a complete end-to-end system that performs **AI-assisted security analysis** on Python code using:

* **OpenAI Agents + MCP servers**
* **Semgrep static analysis integration**
* A **React/Next.js frontend**
* A **FastAPI backend**
* Full **Azure Container Apps deployment** using Terraform
* Automated container builds using Docker

The goal of this project is to deliver a production-grade LLMOps workflow for running, testing, and deploying an AI security analyzer with consistent, repeatable infrastructure.



## 🎥 **Cybersecurity Analyzer Demo**

<div align="center">
  <img src="assets/app/cyber_analyzer.gif" width="100%" alt="Cybersecurity Analyzer Demo">
</div>

This is the fully deployed application running on Azure Container Apps.



## 🧩 **Grouped Stages**

This project consists of **five development and deployment stages**, grouped to reflect the natural progression from initial setup to full cloud deployment.

|  Stage | Category            | Description                                                                                      |
| :----: | ------------------- | ------------------------------------------------------------------------------------------------ |
| **00** | Repository Setup    | Cloning the repository and preparing the project structure                                       |
| **01** | Semgrep & MCP Setup | Creating a Semgrep account, generating API tokens, integrating the MCP server                    |
| **02** | Local Testing       | Running the full application locally (backend + frontend + Docker container test)                |
| **03** | Azure Setup         | Creating the Azure account, setting cost alerts, installing Azure CLI, preparing resource group  |
| **04** | Azure Deployment    | Terraform-based deployment to Azure Container Apps, including ACR image push and service rollout |

This provides a full lifecycle:
**clone → configure → test → prepare cloud → deploy cloud**



## 🗂️ **Project Structure**

```
LLMOps-Cybersecurity-Analyzer/
├── assets/
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
│   ├── azure/
│   │   ├── main.tf
│   │   └── variables.tf
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

The backend performs:

* Semantic analysis through OpenAI Agents
* One-shot Semgrep scanning through MCP server
* Combining static analysis with LLM reasoning
* Validation of requests
* Packaging into structured security reports

### 🖥️ Next.js Frontend (React)

The frontend provides:

* File upload input
* Secure transmission of Python source code
* Real-time analysis status
* Formatted vulnerability table
* Code snippets + recommended fixes
* Summary generation

### 🛠️ MCP + Semgrep

MCP server provides:

* Controlled, rule-safe execution of Semgrep scans
* A strict requirement that Semgrep runs **once per analysis**
* Automatic merging of Semgrep findings + LLM findings

### ☁️ Azure Infrastructure (Terraform)

Terraform automates:

* ACR (Azure Container Registry)
* Building + pushing the Docker image
* Azure Container App environment
* Container App service (1 CPU / 2 GiB required for Semgrep)
* Log Analytics Workspace
* Output of public application URL

This produces a **fully automated, consistent cloud deployment**.



## 💻 **Local Development (Stage 02)**

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



## 🚀 **Azure Deployment (Stage 04)**

### Deployment

```bash
cd terraform/azure

terraform init
terraform workspace new azure
terraform apply \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

### Retrieve URL

```bash
terraform output app_url
```

### Destroy when done

```bash
terraform destroy \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```



## **Summary**

The **LLMOps Cybersecurity Analyzer** is a complete, production-quality example of modern LLMOps engineering:

* Secure AI agent workflows
* Static analysis integration
* Cloud-ready container packaging
* Fully scripted IaC deployment
* Repeatable, scalable, low-cost architecture

This project demonstrates a full lifecycle:
**local development → AI security analysis → MCP + Semgrep integration → IaC cloud deployment**
