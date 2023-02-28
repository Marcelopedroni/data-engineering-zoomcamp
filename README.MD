<h3>This is a Data Engineering Project.</h3>

<p>The main purpose is to study and improve the knowledge on DE by building a data pipeline with a complete infrastructure based on cloud (GCP).
The upcoming contents will be feeding this repo until the project is done (something around 7~10 weeks).</p>

IMPORTANT:
This is part of a free bootcamp, self-called Data Engineering Zoomcamp 2023, made available by [@DataTalksClub](https://github.com/DataTalksClub/data-engineering-zoomcamp/) (for whom I am very very gratefull)

### CONTENTS ###

### Week 1: Introduction & Prerequisites

* Introduction to GCP resources (Storage, BigQuery, VM instances, Billing)
  *Creating Project, VM instance (ssh config connection to access remotely), activating API's, etc*
* Docker and docker-compose
  *First steps with docker and docker-compose*
* Running Postgres locally with Docker (creating an docker image)
  **Persisting data on Postgres instance**
* Setting up infrastructure on GCP with Terraform
  *Creating Storage and BigQuery instances for the project*

### Applied Technologies
* *Google Cloud Platform (GCP)*: Cloud-based auto-scaling platform by Google
  * *Google Cloud Storage (GCS)*
  * *BigQuery*: Data Warehouse
* *Terraform*: Infrastructure-as-Code (IaC)
* *Docker*: Containerization
* *SQL*: Data Analysis & Exploration

### Week 2: Introduction to Prefect concepts

* Prefect flow
* Creating an ETL
* Prefect task
* Blocks and collections
* Orion UI

### Applied Technologies
* *Google Cloud Platform (GCP)*: Cloud-based auto-scaling platform by Google
  * *Google Cloud Storage (GCS)*: Object Storage
  * *BigQuery*: Data Warehouse
* *Docker*: Containerization
* *Prefect*: Orchestrator of flows runs (similar to Airflow, Jenkins) - Free version (hosted locally or on Cloud)

 cmd -> prefect deployment run etl-parent-flow/docker-flow -p "months=[1,2,3,4,5,6,7,8,9,10,11,12]"


### Week 3: BigQuery and DataWarehouse solution

* All discussions were about Google BigQuery for DataWarehouse solution and how to deploy a ML model created in it.
* There were no codes to display, so there is just notes that i've been taken on my notebook. 

### Applied Technologies
* *Google Cloud Platform (GCP)*: Cloud-based auto-scaling platform by Google
  * *Google Cloud Storage (GCS)*: Object Storage
  * *BigQuery*: Data Warehouse and ML solution

  

### More coming soon!