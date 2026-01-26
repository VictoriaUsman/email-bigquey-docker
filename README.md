<img width="1614" height="1088" alt="D0A8CDDE-5AE4-4143-89FA-B205B6366F16" src="https://github.com/user-attachments/assets/59d3b323-c15e-461e-a68a-5b85224000fe" />
<img width="2868" height="1626" alt="E04AD20A-46F5-49EC-8D59-C42DB0FBEFB0" src="https://github.com/user-attachments/assets/ac3ace21-cbfa-4298-bdf7-89a79b6b5458" />


<img width="2918" height="1350" alt="D0E03C16-E0C6-4FB4-A282-7DB13E84B701" src="https://github.com/user-attachments/assets/d6353e12-3461-41bb-ac25-8402f8861ed2" />
<img width="2934" height="952" alt="5EF2AAD7-72B0-4015-AA34-D3AF8D8E51DD" src="https://github.com/user-attachments/assets/12a19b1d-cc4c-4f7a-80ac-50f08f1e2227" />
![Uploading 1B67DD00-3817-48A0-BE7E-4695EE9D2C99.png…]()




# 📊 Email Analytics Data Pipeline (Dagster + Docker)

This project demonstrates a **containerized, production-style data pipeline** that ingests email events, orchestrates processing with **Dagster**, and visualizes analytics in **Power BI**. It is designed as a **data engineering portfolio project** following real-world architecture patterns.

---

## 🏗️ Architecture Overview

```
Email Source → Docker → Dagster → Data Warehouse → Power BI
```

---

## 🔧 Components Explained

### 📧 Email Source

* Gmail / Email API / mock CSV data
* Raw events: sent, opened, clicked, received

### 🐳 Docker (Infrastructure Layer)

* All services run inside containers
* Ensures reproducibility and easy local setup
* Single command startup using docker-compose

### 🧠 Dagster (Orchestration Layer)

* Defines **assets, jobs, and schedules**
* Handles orchestration, retries, and dependencies
* Manages backfills and partitioned data
* Produces clean, validated datasets

### 🗄️ Data Warehouse

* Postgres / BigQuery / Snowflake
* Stores transformed and analytics-ready data
* Partitioned by date for performance

### 📈 Power BI (Visualization)

* Connects directly to the warehouse
* Used for dashboards and reporting
* Auto-refresh enabled

---

## 🔄 Data Flow

1. **Ingest**

   * Email events collected from source

2. **Process & Orchestrate (Dagster)**

   * Schema validation
   * Data cleaning & transformation
   * Asset materialization
   * Scheduling & backfills

3. **Load**

   * Clean data written to warehouse
   * Partitioned by date

4. **Visualize**

   * Power BI dashboards update automatically

---

## 📁 Project Structure

```
.
├── dagster/              # Dagster assets, jobs, schedules
├── scripts/              # ETL logic
├── data/                 # Sample datasets
├── docker-compose.yml    # All services
├── Dockerfile            # Custom Dagster image
└── README.md
```

---

## 🐳 Run Locally

```bash
docker-compose up -d
```

### Access Services

* Dagster UI: [http://localhost:3000](http://localhost:3000)
* Warehouse: localhost:5432

---

## ⚙️ Example Pipeline

```text
extract_email_data → transform_email_data → load_to_warehouse
```

---

## 📊 Example Analytics

* Email volume per day
* Open and click rates
* Processing latency
* Daily trends and spikes

---

## 🧪 Testing Strategy

* Multiple day CSV datasets (backfill testing)
* Partitioned assets (daily)
* Idempotent runs
* Late-arriving data simulation
* Schema drift handling

---

## 🎯 Skills Demonstrated

* Dagster orchestration (assets, schedules, sensors)
* Docker & containerization
* ETL / ELT best practices
* Partitioned data modeling
* Analytics engineering
* BI integration (Power BI)

---

## 👤 Author

**Ian Tristan**
Aspiring Data Engineer | Dagster | Docker | Analytics

---






