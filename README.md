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

Terraform reads the API keys from environment variables.
Load them from your `.env` file:

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

Initialise Terraform and create the Azure workspace:

```bash
terraform init
terraform workspace new azure
terraform workspace select azure
terraform workspace show
```

You should now see Terraform initialise the Azure provider and confirm you are in the `azure` workspace.



## **Step 4: Login to Azure & Register Providers**

Login through Azure CLI:

```bash
az login
az account show --output table
```

Ensure the correct subscription is shown.

### Why register resource providers?

Azure requires explicit activation of certain services (unlike AWS, where most are enabled once IAM is set).
You must register these **once per subscription**.

Register the required providers:

```bash
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
```

Check their status:

```bash
az provider show --namespace Microsoft.App --query "registrationState" -o tsv
az provider show --namespace Microsoft.OperationalInsights --query "registrationState" -o tsv
```

Make sure both show **Registered** before proceeding.



## **Step 5: Deploy to Azure**

### Plan the deployment:

```bash
terraform plan \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

You should see creation of:

* ACR (Azure Container Registry)
* Log Analytics workspace
* Container Apps environment
* Container App itself
* Docker image build + push

### Apply the deployment

**Mac/Linux:**

```bash
terraform apply \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

**Windows PowerShell:**

```powershell
terraform apply -var ("openai_api_key=" + $Env:OPENAI_API_KEY) -var ("semgrep_app_token=" + $Env:SEMGREP_APP_TOKEN)
```

Type **yes** when prompted.
This takes around 5–10 minutes.

### Forcing a rebuild after code changes

If Terraform doesn’t pick up code changes:

```bash
terraform taint docker_image.app
terraform taint docker_registry_image.app
```

Then re-run `terraform apply`.



## **Step 6: Retrieve Your Application URL**

```bash
terraform output app_url
```

Example:

```
"https://cyber-analyzer.nicehill-12345678.eastus.azurecontainerapps.io"
```

🎉 Your Azure-hosted application is now live!



## **Step 7: Verify the Deployment**

### Test the Live Application

1. Open the URL in a browser
2. The Cybersecurity Analyzer UI should appear
3. Upload a Python file and run analysis
4. Confirm full end-to-end functionality

assets/app/cyber_analyzer.gif

### Check Azure Resources

In Azure Portal:

1. Open the **cyber-analyzer-rg** resource group
2. You should see:

   * ACR
   * Log Analytics Workspace
   * Container Apps Environment
   * Container App

assets/azure/resources.png

### View Live Logs

```bash
az containerapp logs show --name cyber-analyzer --resource-group cyber-analyzer-rg --follow
```

### Check Costs

In Azure Portal:

1. Search for **Cost Management**
2. Open **Cost analysis**
3. Filter by resource group `cyber-analyzer-rg`



## **Step 8: Clean Up Resources (Important)**

Azure resources cost money even when idle, so destroy everything after each lab session.

### Destroy all resources

**Mac/Linux:**

```bash
terraform destroy \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

**Windows PowerShell:**

```powershell
terraform destroy -var ("openai_api_key=" + $Env:OPENAI_API_KEY) -var ("semgrep_app_token=" + $Env:SEMGREP_APP_TOKEN)
```

Type **yes** to confirm.

### Optional: Delete the resource group entirely

```bash
az group delete --name cyber-analyzer-rg --yes
```



## **Understanding Your Azure Architecture**

### Cost Summary (very low for learning)

* **ACR Basic Tier**: ~$5/month
* **Container Apps**: ~$0 when scaled to zero
* **Log Analytics**: 5GB free/month
* **Total**: < $5/month

### Deployment Architecture

```
Internet → Azure Container App → Your Docker Image
                 ↓
          Log Analytics
                 ↓
       Azure Container Registry
```

### Scaling Behaviour

* **Min replicas**: 0
* **Max replicas**: 1
* **Autoscaling**: HTTP-triggered
