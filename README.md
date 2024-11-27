# Notion Movie Name Automation

## Overview

**Notion Movie Name Automation** is a project that automates the process of fetching movie names from Notion using the Notion API. It utilizes BeautifulSoup4 to scrape movie URLs and serves the results through a FastAPI application. The FastAPI application is hosted on an AWS EC2 instance, which is provisioned using Terraform and configured with Ansible.

## Features

- Fetch movie names from Notion using the Notion API.
- Scrape movie URLs using BeautifulSoup4.
- Serve the data through a FastAPI application.
- Deploy the application on AWS EC2 using Terraform.
- Configure the EC2 instance using Ansible for easy setup and management.

## Technologies Used

- **Notion API**: For fetching movie names.
- **BeautifulSoup4**: For web scraping movie URLs.
- **FastAPI**: For building the web application.
- **Terraform**: For provisioning AWS resources.
- **Ansible**: For configuring the EC2 instance.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)
- Terraform
- Ansible
- AWS CLI (configured with your credentials)

## Environment Variables

TOKEN_ID=
DATABASE_ID=
PORT=8000
JWT_SECRET=
DB_URI=

### Installation

**NOTE**
Make sure to change the --private-key file to point to where your private is located

1. **Clone the repository**:

   ```bash
     git clone https://github.com/yourusername/notion-movie-name-automation.git
     cd notion-movie-name-automation
   ```

2. **Create a Python environment using Conda or venv or Pipenv**:
   ```bash
    pipenv install -r requirements.txt
   ```
3. **Install Terraform, Ansible, Docker, and AWS-cli:**
   ```bash
    brew install ansible terraform aws-cli docker docker-desktop
   ```
4. **Setup your AWS Configuration and Ansible-Galaxy module:**

```bash
  aws configure
  ansible-galaxy collection install amazon.aws
```

5. **Run script.sh:**

```bash
  sh script.sh
```
