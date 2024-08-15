# ELT Tool for Brazilian E-Commerce Data Analysis

This project develops an automated Extract, Load, Transform, and Model (ELT) pipeline for Brazilian E-Commerce orders data obtained from the Alist Store on Kaggle. The tool leverages a combination of technologies to achieve an end-to-end data engineering workflow.

## Project Overview

- **PostgreSQL:** Stores the raw data.
- **Docker & Docker Compose:** Manages containerized applications.
- **Apache Airflow:** Orchestrates the ETL tasks.
- **dbt (Data Build Tool):** Transforms and models data in BigQuery.
- **Google Cloud Bucket (Optional):** Can be used for temporary data storage.
- **BigQuery:** The final data warehouse for analysis.
- **Python:** Scripting language used for data manipulation and ETL logic.

## Project Goals

- Develop a scalable ELT pipeline for e-commerce data.
- Utilize Airflow for scheduling and orchestration.
- Model data for analytical queries using dbt.

## Getting Started

Before starting, ensure you have the following prerequisites:

### Prerequisites

- Docker and Docker Compose installed on your local machine.
- A Google Cloud Platform (GCP) project with the BigQuery API enabled.
- Python installed on your local machine (version 3.7 or later).

<img width="518" alt="image" src="https://github.com/user-attachments/assets/0a8d6d13-4ce8-4b5a-b532-6626649747b9">


### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ififrank2013/ELT-Tool-for-Data-Analysis-Capstone-Project.git
    cd ELT-Tool-for-Data-Analysis-Capstone-Project
    ```

2. **Set up your environment:**

    Ensure you have a `.env` file in the root directory with the necessary environment variables. You can use `.sample.env` as a template.

3. **Install Python dependencies:**

    Install the required Python packages using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

4. **Build Docker images:**

    Build the Docker containers for PostgreSQL and Airflow:

    ```bash
    docker-compose build
    ```

5. **Start the services:**

    Start the services defined in the `docker-compose.yml`:

    ```bash
    docker-compose up -d
    ```

6. **Access Airflow:**

    Access the Airflow web UI at [http://localhost:9090](http://localhost:9090) (default username: `airflow`, password: `airflow`).

