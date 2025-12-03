# 🛡️ LLMOps Cybersecurity Analyzer — Repository Setup

This branch covers the initial setup—getting the project onto your machine and opening it in your editor so you can explore the structure.

## Step 1: Clone the Repository

Begin by cloning the project from GitHub:

```bash
git clone https://github.com/Ch3rry-Pi3-AI/LLMOps-Cybersecurity-Analyzer.git
cd LLMOps-Cybersecurity-Analyzer
```

This downloads the project and moves you into the root directory.

## Step 2: Open the Project in VS Code (or Cursor)

1. Launch VS Code or Cursor
2. Select **File → New Window**
3. Select **File → Open Folder**
4. Find and select the `LLMOps-Cybersecurity-Analyzer` folder
5. Click **Open**

Your editor will load the full project structure.

## Step 3: Explore the Project Structure

You should now see a layout similar to:

```
LLMOps-Cybersecurity-Analyzer/
  ├─ assets/
  │   └─ README.md
  ├─ backend/
  │   ├─ context.py
  │   ├─ mcp_servers.py
  │   ├─ server.py
  │   ├─ pyproject.toml
  │   └─ README.md
  ├─ frontend/
  │   ├─ public/
  │   ├─ src/
  │   └─ README.md
  ├─ terraform/
  │   ├─ azure/
  │   │   ├─ main.tf
  │   │   └─ variables.tf
  │   └─ gcp/
  │       ├─ main.tf
  │       ├─ variables.tf
  │       └─ allow-all-policy.yaml
  ├─ airline.py
  ├─ Dockerfile
  ├─ .dockerignore
  ├─ .gitignore
  ├─ .python-version
  ├─ uv.lock
  ├─ package.json
  ├─ package-lock.json
  ├─ next.config.ts
  ├─ tsconfig.json
  └─ README.md
```

Key components:

* **frontend/** — Next.js React interface
* **backend/** — FastAPI service powering the security analysis
* **terraform/** — IaC for Azure and GCP deployment
* **airline.py** — additional experimental agent example
