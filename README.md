<img width="1612" height="1046" alt="FDFF5331-90AD-4BEC-9683-66F9588A47D5" src="https://github.com/user-attachments/assets/3e1ab382-81db-4108-a825-c44a1381a5e8" />
# 📊 Email Analytics Data Pipeline (Dockerized)

This project demonstrates a **containerized data pipeline** that ingests email events, processes them using a workflow orchestrator, and visualizes analytics in a BI tool. It is designed as a **data engineering portfolio project** and can be run locally using Docker.

---

## 🏗️ Architecture Overview

```
Email Source → Docker → Airflow → Data Warehouse → Power BI
```

### Components

* **Email Source (Gmail / Email API)**

  * Acts as the raw data source (email events, notifications, logs, etc.)

* **Docker**

  * All services are containerized for easy setup and reproducibility

* **Apache Airflow**

  * Orchestrates the pipeline
  * Handles scheduling, retries, and dependencies
  * Runs ETL tasks inside containers

* **Data Warehouse (Postgres / BigQuery / Snowflake)**

  * Stores cleaned and transformed data
  * Optimized for analytics queries

* **Power BI**

  * Connects to the warehouse
  * Used for dashboards and reporting

---

## 🔄 Data Flow

1. **Ingestion**

   * Airflow pulls email data from the source (API / export / mock data)

2. **Processing**

   * Data is cleaned, validated, and transformed
   * Timestamps normalized
   * Schema enforced

3. **Loading**

   * Transformed data is written to the warehouse
   * Partitioned by date for performance

4. **Visualization**

   * Power BI reads from the warehouse
   * Dashboards update automatically

---

## 🐳 Docker Setup

All services run in Docker containers:

* `airflow-webserver`
* `airflow-scheduler`
* `postgres` (metadata DB)
* `warehouse` (analytics DB)

```bash
docker-compose up -d
```

---

## 📁 Project Structure

```
.
├── dags/                # Airflow DAGs
├── scripts/             # ETL scripts
├── data/                # Sample datasets
├── docker-compose.yml   # Service definitions
├── Dockerfile           # Custom Airflow image
└── README.md
```

---

## ⚙️ Example DAG Flow

```text
extract_email_data → transform_data → load_to_warehouse
```

Each task runs in isolation and is fully retryable.

---

## 📈 Analytics Use Cases

* Email volume per day
* Open / click rates
* Processing latency
* Event trends over time

---

## 🧪 Testing

* Local CSV datasets for backfill testing
* Multiple days of data for partition validation
* Idempotent DAG runs

---

## 🚀 How to Run

1. Clone repository

   ```bash
   git clone <repo-url>
   cd project
   ```

2. Start services

   ```bash
   docker-compose up -d
   ```

3. Open Airflow

   ```
   http://localhost:8080
   ```

4. Run DAG and refresh Power BI

---

## 🎯 Skills Demonstrated

* Data pipeline design
* Apache Airflow orchestration
* Docker & containerization
* ETL / ELT best practices
* Analytics engineering
* BI integration

---

## 📌 Notes

This project is built for learning and portfolio purposes but follows real-world data engineering patterns.

---

## 👤 Author

**Ian Tristan**
Aspiring Data Engineer | Cloud | ETL | Analytics


