# ☁️ **LLMOps Cybersecurity Analyzer — GCP Cloud Run Deployment**

This branch covers deploying the Cybersecurity Analyzer to **Google Cloud Run** using **Terraform**.
The workflow automatically builds your Docker image, pushes it to Google Container Registry, and deploys a fully serverless Cloud Run service.

## **Step 1: Prerequisites**

Before beginning, make sure you have:

* Completed the GCP setup stage
* Terraform installed
* Docker running locally
* A `.env` file in the project root containing:

  * `OPENAI_API_KEY`
  * `SEMGREP_APP_TOKEN`
* Your **GCP Project ID** (example: `cyber-analyzer-123456`)

### Quick Terraform Check

```bash
terraform version
```

If Terraform is not installed:

* **Mac:** `brew install terraform`
* **Windows:** Download from [https://terraform.io/downloads](https://terraform.io/downloads)
* **Linux:** See Terraform docs for apt/yum installation guides

## **Step 2: Get Your Project ID**

You must use the **project ID**, not the project name.

```bash
gcloud projects list
```

Example output:

```
PROJECT_ID              NAME             PROJECT_NUMBER
cyber-analyzer-123456   cyber-analyzer   123456789012
```

Copy your `PROJECT_ID` — you'll need it shortly.

## **Step 3: Set Environment Variables**

Terraform reads keys via environment variables.

### Mac / Linux

```bash
export $(cat .env | xargs)

export TF_VAR_project_id="cyber-analyzer-123456"

echo "Project ID: $TF_VAR_project_id"
echo "OpenAI key loaded: ${OPENAI_API_KEY:0:8}..."
echo "Semgrep token loaded: ${SEMGREP_APP_TOKEN:0:8}..."
```

### Windows PowerShell

```powershell
Get-Content .env | ForEach-Object {
    $name, $value = $_.split('=', 2)
    Set-Item -Path "env:$name" -Value $value
}

$env:TF_VAR_project_id = "cyber-analyzer-123456"

Write-Host "Project ID: $env:TF_VAR_project_id"
Write-Host "OpenAI key loaded: $($env:OPENAI_API_KEY.Substring(0,8))..."
Write-Host "Semgrep token loaded: $($env:SEMGREP_APP_TOKEN.Substring(0,8))..."
```

## **Step 4: Initialise Terraform**

Navigate to the GCP Terraform directory:

```bash
cd terraform/gcp
```

Initialise Terraform and create/select the workspace:

```bash
terraform init
terraform workspace new gcp
terraform workspace select gcp
terraform workspace show
```

You should now see the `gcp` workspace active.

## **Step 5: Authenticate with Google Cloud**

Authenticate and configure your environment for Cloud Run deployments:

```bash
gcloud auth login
gcloud config set project $TF_VAR_project_id
gcloud auth application-default login
gcloud auth application-default set-quota-project $TF_VAR_project_id
gcloud auth configure-docker
gcloud config list
```

Ensure the project displayed matches your project ID.

## **Step 6: Deploy to Cloud Run**

### Plan the deployment first

Mac / Linux:

```bash
terraform plan \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

Windows PowerShell:

```powershell
terraform plan -var ("openai_api_key=" + $Env:OPENAI_API_KEY) -var ("semgrep_app_token=" + $Env:SEMGREP_APP_TOKEN)
```

You should see Terraform preparing:

* Cloud Run API
* Container Registry API
* Cloud Build API
* Docker image build + push
* Cloud Run service
* Public access

### Apply and deploy

Mac / Linux:

```bash
terraform apply \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

Windows PowerShell:

```powershell
terraform apply -var ("openai_api_key=" + $Env:OPENAI_API_KEY) -var ("semgrep_app_token=" + $Env:SEMGREP_APP_TOKEN)
```

Type `yes` when prompted.

Terraform will:

1. Enable APIs
2. Build your Docker image
3. Push it to Container Registry
4. Deploy Cloud Run
5. Open public access permissions

### Forcing a rebuild after code changes

```bash
terraform taint docker_image.app
terraform taint docker_registry_image.app
```

Then re-run `terraform apply`.

## **Step 7: Get Your Cloud Run URL**

```bash
terraform output service_url
```

Example:

```
"https://cyber-analyzer-abcdef123-uc.a.run.app"
```

Your application is now live.

## **Step 8: Verify Deployment**

### Test your live app

1. Open the URL
2. The Cybersecurity Analyzer UI should load
3. Upload a Python file
4. Confirm vulnerability detection works end-to-end

### Check Cloud Console resources

1. Go to [https://console.cloud.google.com](https://console.cloud.google.com)
2. Select your project
3. Navigate to **Cloud Run**
4. Confirm the `cyber-analyzer` service is deployed

### Logs

```bash
gcloud run services logs read cyber-analyzer --limit=50 --region=$TF_VAR_region

gcloud alpha run services logs tail cyber-analyzer --region=$TF_VAR_region
```

## **Step 9: Clean Up Resources**

Always destroy resources to avoid charges from:

* Cloud Run
* Container Registry storage
* Cloud Build

### Destroy everything

Mac / Linux:

```bash
terraform destroy -var="openai_api_key=$OPENAI_API_KEY" -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

Windows PowerShell:

```powershell
terraform destroy -var ("openai_api_key=" + $Env:OPENAI_API_KEY) -var ("semgrep_app_token=" + $Env:SEMGREP_APP_TOKEN)
```

Type `yes` when prompted.

This removes:

* Cloud Run service
* Container Registry image
* IAM policies
* Terraform-managed configuration