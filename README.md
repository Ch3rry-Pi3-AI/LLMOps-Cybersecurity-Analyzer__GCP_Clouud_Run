# 🧩 LLMOps Cybersecurity Analyzer — Microsoft Azure Setup

This branch README walks you through preparing your Azure account so you can deploy the Cybersecurity Analyzer in later stages. All essential steps are included, and the structure matches your preferred style.

## Step 1: Create Your Azure Account

### Azure Free Account

1. Visit: **[https://azure.microsoft.com/en-us/free/](https://azure.microsoft.com/en-us/free/)**
2. Click **“Start free”**
3. Sign in with your Microsoft account (or create one)
4. Provide:

   * A credit card (identity verification only — not charged)
   * A phone number
5. You’ll receive:

   * $200 credit for 30 days
   * 12 months of free popular services
   * Always-free tier services

**Note:** If you have a **.edu** email, you may qualify for *Azure for Students* with $100 free credit and **no credit card needed**:
[https://azure.microsoft.com/en-us/free/students/](https://azure.microsoft.com/en-us/free/students/)

Once your account is created, you’ll be redirected to the Azure Portal:
[https://portal.azure.com](https://portal.azure.com)

## Step 2: Understand Azure’s Structure

Before creating anything, it's useful to understand how Azure organizes resources:

```
Azure Account (your email)
  └── Subscription (billing boundary)
      └── Resource Group (project folder)
          └── Resources (Container Apps, Registries, Logs, Networks)
```

Think of it like this:

* **Subscription** → Your payment boundary
* **Resource Group** → Logical container for related resources
* **Resources** → The actual services you deploy

## Step 3: Set Up Cost Management

Let’s create a budget so you never overspend accidentally:

1. Open the Azure Portal: [https://portal.azure.com](https://portal.azure.com)
2. Use the search bar → type **Cost Management + Billing**
3. Click **Cost Management**
4. Select **Budgets**
5. Click **+ Add**
6. Configure:

   * Name: `Monthly-Training-Budget`
   * Reset period: Monthly
   * Budget amount: `10`
   * Click **Next**
7. Add email alerts for:

   * 50% usage
   * 80% usage
   * 100% usage
8. Enter your email
9. Click **Create**

Now you’ll receive warning emails as you approach your budget.

## Step 4: Create Your First Resource Group

All Azure resources for this project must live inside a resource group.

1. In the Azure Portal, click the **☰ menu** (top-left)
2. Choose **Resource groups**
3. Click **+ Create**
4. Fill these fields:

   * **Subscription** → Your subscription
   * **Resource group** → `cyber-analyzer-rg`
   * **Region** → Choose the closest region to reduce latency

Examples:

* **US** → East US, West US 2
* **Europe** → West Europe, North Europe
* **Asia** → Southeast Asia, Japan East

**Tip:** Keep all resources in the same region for best performance and lowest cost.

5. Click **Review + create**
6. Click **Create**

Your first resource group is now ready.

## Step 5: Install Azure CLI

Azure CLI allows you to deploy containers, create services, and automate infrastructure.

### Windows

1. Download installer: [https://aka.ms/installazurecliwindows](https://aka.ms/installazurecliwindows)
2. Run the MSI
3. Restart your terminal

### macOS

**Option 1 — Homebrew**

```bash
brew update && brew install azure-cli
```

**Option 2 — Direct installer**

1. Download: [https://aka.ms/installazureclimacos](https://aka.ms/installazureclimacos)
2. Install the `.pkg`
3. Follow the wizard

### Verify Installation

Run:

```bash
az --version
```

You should see version details.

### Login to Azure

```bash
az login
```

A browser will open. Log in with your Azure account.

## Step 6: Verify Your Setup

### Using Azure Portal

1. Visit [https://portal.azure.com](https://portal.azure.com)
2. Search for `cyber-analyzer-rg`
3. Click the group
4. You should see:

   * Correct region
   * Empty resource list (expected at this stage)

### Using Azure CLI

```bash
# Show your Azure subscriptions
az account list --output table

# Show your resource groups
az group list --output table
```

If everything is configured correctly, you’ll see your subscription and your `cyber-analyzer-rg` group.
