# 🧪 LLMOps Cybersecurity Analyzer — Local Testing (Without & With Docker)

This branch README walks you through testing the application locally in two ways:

1. Running the **backend and frontend directly** on your machine
2. Running the **containerized version** that mirrors cloud deployment

## Step 1: Test Locally Without Docker

Let’s first run the system directly on your machine.

### Prerequisites Check

Verify the required tools:

```bash
# Check Node.js (should be version 20+)
node --version

# Check uv (Python package manager)
uv --version
```

If `uv` is missing:

```bash
# Mac/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell as Admin)
irm https://astral.sh/uv/install.ps1 | iex
```

### Start the Backend Server

Open a new terminal in Cursor and run:

```bash
cd backend
uv run server.py
```

Expected output:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

The backend is now live at:

```
http://localhost:8000
```

### Start the Frontend Development Server

Open **another terminal** and run:

```bash
cd frontend
npm install    # Only required the first time
npm run dev
```

You should see Next.js start up:

```
  ▲ Next.js 15.x.x
  - Local:        http://localhost:3000
  - Environments: .env

✓ Ready in 2.1s
```

### Test the Application

1. Open your browser at:

```
http://localhost:3000
```

2. You should see the Cybersecurity Analyzer UI:

3) Click **“Choose File”** and upload the `airline.py` file in the project root
4) Click **“Analyze Code”**
5) You should see security vulnerabilities detected:

### Stopping Local Servers

* Stop backend: press `Ctrl + C` in its terminal
* Stop frontend: press `Ctrl + C` in its terminal

Now you're ready to test the containerized version.

## Step 2: Test Locally With Docker

### Prerequisites Check

Ensure Docker is properly installed:

```bash
docker --version
docker ps
```

If these fail, install Docker Desktop:
[https://docker.com/get-started](https://docker.com/get-started)

### Build the Docker Image

From the root of the project:

```bash
docker build -t cyber-analyzer .
```

The first build takes a few minutes. You’ll see:

```
Successfully tagged cyber-analyzer:latest
```

### Run the Container

Start the fully packaged system:

```bash
docker run --rm --name cyber-analyzer -p 8000:8000 --env-file .env cyber-analyzer
```

Meaning of flags:

* `--rm` → Delete container on exit
* `--name` → Easier reference
* `-p 8000:8000` → Expose backend
* `--env-file .env` → Load API keys
* `cyber-analyzer` → Image name

Expected startup logs:

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Test the Container

1. Open:

```
http://localhost:8000
```

2. Upload the same `airline.py` file
3. You should see identical results to non-Docker mode

### Stop the Container

Press `Ctrl + C` in the Docker terminal — the container will auto-remove thanks to `--rm`.