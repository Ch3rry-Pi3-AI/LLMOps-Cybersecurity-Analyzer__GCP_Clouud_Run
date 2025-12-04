# ☁️ **LLMOps Cybersecurity Analyzer — Azure Deployment**

This branch covers deploying the Cybersecurity Analyzer to **Microsoft Azure Container Apps** using **Terraform**.
You will build the Docker image, push it to Azure Container Registry, and deploy it as a serverless containerised application.

## **Step 1: Prerequisites**

Before beginning, make sure you have:

* Completed the earlier setup stages
* Terraform installed
* Docker running locally
* A `.env` file in the project root containing:

  * `OPENAI_API_KEY`
  * `SEMGREP_APP_TOKEN`

### Quick Terraform Check

```bash
terraform version
```

If you need to install Terraform:

* **Mac (Homebrew):**
  `brew install terraform`

* **Windows:**
  Download from [https://terraform.io/downloads](https://terraform.io/downloads)

## **Step 2: Set Environment Variables**

### Mac / Linux

```bash
export $(cat .env | xargs)

echo "OpenAI key loaded: ${OPENAI_API_KEY:0:8}..."
echo "Semgrep token loaded: ${SEMGREP_APP_TOKEN:0:8}..."
```

### Windows (PowerShell)

```powershell
Get-Content .env | ForEach-Object {
    $name, $value = $_.split('=', 2)
    Set-Item -Path "env:$name" -Value $value
}

Write-Host "OpenAI key loaded: $($env:OPENAI_API_KEY.Substring(0,8))..."
Write-Host "Semgrep token loaded: $($env:SEMGREP_APP_TOKEN.Substring(0,8))..."
```

## **Step 3: Initialise Terraform**

Navigate to the Azure Terraform directory:

```bash
cd terraform/azure
```

Init and create workspace:

```bash
terraform init
terraform workspace new azure
terraform workspace select azure
terraform workspace show
```

## **Step 4: Login to Azure & Register Providers**

```bash
az login
az account show --output table
```

Register required providers:

```bash
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
```

Check they’re registered:

```bash
az provider show --namespace Microsoft.App --query "registrationState" -o tsv
az provider show --namespace Microsoft.OperationalInsights --query "registrationState" -o tsv
```

## **Step 5: Deploy to Azure**

### Plan:

```bash
terraform plan \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

### Apply:

**Mac/Linux**

```bash
terraform apply \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

**Windows PowerShell**

```powershell
terraform apply -var ("openai_api_key=" + $Env:OPENAI_API_KEY) -var ("semgrep_app_token=" + $Env:SEMGREP_APP_TOKEN)
```

### Force rebuild after code changes

```bash
terraform taint docker_image.app
terraform taint docker_registry_image.app
```

## **Step 6: Retrieve Your Application URL**

```bash
terraform output app_url
```

Example:

```
"https://cyber-analyzer.nicehill-12345678.eastus.azurecontainerapps.io"
```

## **Step 7: Verify the Deployment**

### Test the application

assets/app/cyber_analyzer.gif

### Check Azure resources

assets/azure/resources.png

### Logs

```bash
az containerapp logs show --name cyber-analyzer --resource-group cyber-analyzer-rg --follow
```

### Costs

Check in Azure Portal under **Cost Management → Cost analysis**.

## **Step 8: Clean Up Resources**

### Destroy everything

**Mac/Linux**

```bash
terraform destroy \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

**Windows PowerShell**

```powershell
terraform destroy -var ("openai_api_key=" + $Env:OPENAI_API_KEY) -var ("semgrep_app_token=" + $Env:SEMGREP_APP_TOKEN)
```

### Optional: delete resource group

```bash
az group delete --name cyber-analyzer-rg --yes
```

## **Understanding the Azure Architecture**

### Cost Summary

* ACR Basic: ~$5/mo
* Container Apps: ~$0 when idle
* Log Analytics: 5GB free
* Total: < $5/month

### Architecture

```
Internet → Azure Container App → Your Docker Image
                 ↓
          Log Analytics
                 ↓
       Azure Container Registry
```

### Scaling

* Min replicas: 0
* Max replicas: 1
