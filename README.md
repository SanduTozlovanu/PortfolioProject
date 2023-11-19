# PortfoPal

## Overview

This project is built on a microservice architecture using the Flask Python framework for the backend and React for the frontend. For an in-depth understanding, refer to the comprehensive document, "BachelorTozlovanuSandu.pdf," covering internal details, architecture, technology stack, and design decisions.

**Disclaimer**: To ensure proper functionality, an API key from [FinancialModelingPrep](https://site.financialmodelingprep.com/) is required, available through their Starter pack at $30 per month.

## Steps to Configure and Start the Project

### Step 1: Obtain API Key

- Visit [FinancialModelingPrep](https://site.financialmodelingprep.com/developer/docs/pricing) and subscribe to the Starter pack to acquire the API key.

### Step 2: Clone the Project

- Clone the project from GitHub into your preferred Integrated Development Environment (IDEA) using the following command:
  ```bash
  git clone <project_repository_url>
### Step 3: Install Python Dependencies

- Open the terminal at the project path and install Python dependencies:
  ```bash
  pip install -r requirements.txt

### Step 4: Install React Dependencies

- Navigate to the React frontend directory:
  ```bash
  cd FrontEnd/react-admin/src
- Install React dependencies:
  ```bash
  npm install
  
### Step 5: Configure API Key

- Locate the configuration file at "projectPath/publicServer/config/config.ini"
- Replace the string "your_financialmodelingprep.com_api_key" with your FinancialModelingPrep API key.

### Step 6: Start Servers

- Run the following commands to start servers:
- Start publicServer:
  ```bash
  python publicServer/server.py
  ```
- Start privateServer:
  ```bash
  python privateServer/server.py
  ```
- Start portfolioCreatorsServer:
  ```bash
  python portfolioCreatorsServer/server.py
  ```

### Step 7: Start Frontend
- Navigate to the React frontend directory:
  ```bash
  cd FrontEnd/react-admin/src
- Start the FrontEnd project
  ```bash
  npm start
## Final Notes

- Upon completing these steps, the application should be up and running. For any queries or assistance, feel free to reach out. Good luck!
