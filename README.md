
#  Network Security System – End-to-End MLOps with ETL

##  1. Overview

The **Network Security System** is a **production-grade MLOps project** built to detect **phishing or malicious websites** (a form of network intrusion) using a **fully automated machine learning pipeline**.

It follows the **complete MLOps lifecycle**, covering every phase —
**Data Ingestion → Validation → ETL/Preprocessing → Model Training → Artifact Management → API Inference → CI/CD → Cloud Deployment → Experiment Tracking.**

This project integrates **data engineering**, **machine learning**, **API development**, and **cloud automation**, making it an excellent **end-to-end industry-level portfolio project**.

---

##  Quick Links

* **GitHub Repo:** [Network Security System – MLOps with ETL](https://github.com/28Deepakpandey/Network-Security-System-MLOps-Project-with-ETL-)
* **Experiment Tracking:** [DagsHub Dashboard](https://dagshub.com/deepakpandey28july/Network-Security-System-MLOps-Project-with-ETL-/experiments)
* **Local API Docs (FastAPI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

##  2. Project Objectives

* Build an **automated ML pipeline** that continuously processes and analyzes network/URL data.
* Detect **phishing and malicious websites** based on multiple URL-based features.
* Enable **one-click retraining and inference** through APIs.
* Ensure **reproducibility**, **scalability**, and **maintainability** of the ML workflow using **MLOps principles**.
* Deploy the entire system to the **cloud** using Docker and **CI/CD with GitHub Actions + AWS**.

---

##  3. Why This Project

This project is designed to **demonstrate MLOps best practices** and show how a real-world ML application is built, automated, deployed, and monitored.

**Key reasons and learning outcomes:**

* Hands-on experience in **ETL + ML + DevOps integration**.
* Covers the **complete lifecycle** of a model — from raw data to production API.
* Implements **version control for data, models, and experiments**.
* **Cloud-native deployment** with containerization and CI/CD automation.
* Perfect for **interviews, resumes, or technical portfolios** showcasing ML system design.

---

##  4. Dataset Overview

The dataset contains **30 features** extracted from website URLs. Each record represents a website and its characteristics (e.g., IP presence, HTTPS token, number of subdomains, etc.)

**Target column:** `Result`

* `-1 → Phishing/Malicious`
* `1 → Legitimate Website`

### Example Columns

```
having_IP_Address, URL_Length, Shortining_Service, having_At_Symbol,
double_slash_redirecting, Prefix_Suffix, having_Sub_Domain, SSLfinal_State,
Domain_registeration_length, Favicon, port, HTTPS_token, Request_URL, 
URL_of_Anchor, Links_in_tags, SFH, Submitting_to_email, Abnormal_URL, Redirect, 
on_mouseover, RightClick, popUpWidnow, Iframe, age_of_domain, DNSRecord, 
web_traffic, Page_Rank, Google_Index, Links_pointing_to_page, Statistical_report, Result
```

### Sample Rows

| having_IP_Address | URL_Length | ... | Result |
| ----------------- | ---------- | --- | ------ |
| -1                | 1          | ... | -1     |
| 1                 | 1          | ... | 1      |

> **Note:** Always keep your schema definition (`data_schema/schema.yaml`) aligned with the dataset columns. The ingestion and validation stages rely on this schema.

---

##  5. Architecture & Pipeline

**Textual Flow of the Pipeline:**

```
Raw Data (CSV / push_data.py)
        ↓
MongoDB Atlas (Data Lake)
        ↓
data_ingestion.py          → Load data into Pandas
        ↓
data_validation.py         → Check schema & missing values
        ↓
data_transformation.py     → ETL: Clean, Encode, Scale, Prepare
        ↓
model_trainer.py           → Train + Evaluate + Save models
        ↓
final_model/               → Save preprocessor.pkl + model.pkl
        ↓
app.py (FastAPI)           → Serve /train and /predict APIs
        ↓
Dockerize → Push to ECR → Deploy to EC2 → Track via DagsHub (MLflow)
```

This pipeline ensures **automation, reproducibility, and versioning** at every stage.

---

##  6. Project Structure

```
Network-Security/
│
├── app.py                          # FastAPI application (train/predict endpoints)
├── main.py                         # Entry point for local training
├── requirements.txt                 # Python dependencies
├── Dockerfile                      # Docker build configuration
│
├── data_schema/
│   └── schema.yaml                 # Column schema for data validation
│
├── networksecurity/
│   ├── components/                 # Core pipeline stages
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   │
│   ├── pipeline/                   # Orchestration logic
│   │   └── training_pipeline.py
│   │
│   ├── utils/                      # Helper utilities (I/O, preprocessing)
│   ├── logging/                    # Centralized logger setup
│   ├── exception/                  # Custom error classes
│   └── cloud/                      # Future cloud integration modules
│
├── final_model/                    # Saved artifacts (preprocessor, model)
├── Network_Data/                   # Local dataset storage
├── prediction_output/              # Stores prediction CSV outputs
├── push_data.py                    # Push local CSV to MongoDB Atlas
├── test_mongodb.py                 # Check MongoDB connectivity
└── .github/workflows/              # CI/CD automation scripts
```

---

##  7. Setup & Run

###  Prerequisites

* Python 3.9+
* Docker (for containerized deployment)
* AWS CLI (for CI/CD pipeline)
* MongoDB Atlas account

###  Steps

#### 1️ Clone Repository

```bash
git clone https://github.com/28Deepakpandey/Network-Security.git
cd Network-Security
```

#### 2️ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### 3️ Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4️ Setup Environment Variables

Create a `.env` file in the project root:

```
MONGODB_URL_KEY="mongodb+srv://<user>:<password>@<cluster>/<db>?retryWrites=true&w=majority"
```

#### 5️ Push Dataset to MongoDB (optional)

```bash
python push_data.py
```

#### 6️ Train the Model

```bash
python main.py
# or through API:
GET http://127.0.0.1:8000/train
```

#### 7️ Predict from API

```bash
python app.py
# Swagger UI:
http://127.0.0.1:8000/docs
```

Upload a CSV file via `/predict` → results are stored in `prediction_output/output.csv`.

---

##  8. Model & Preprocessing Details

* **Preprocessing Steps:**

  * Handle missing values
  * Encode categorical columns
  * Scale numeric columns
  * Save preprocessor (`preprocessor.pkl`)

* **Models Tried:**

  * Logistic Regression
  * Random Forest
  * **XGBoost (Final Model)**

* **Evaluation Metrics:**

  * Accuracy, Precision, Recall, F1-Score, ROC-AUC

All metrics and artifacts are logged in **DagsHub** for experiment tracking.

---

##  9. CI/CD & Cloud Deployment

Automated CI/CD using **GitHub Actions + AWS (ECR + EC2):**

1. On push to `main`, workflow triggers:

   * Run lint/tests
   * Build Docker image
   * Push image to **AWS ECR**
   * SSH into **EC2**, pull new image, and run container

**Secrets in GitHub:**

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
ECR_REPOSITORY
EC2_HOST
EC2_USER
EC2_SSH_KEY
```

**Deployment command (example):**

```bash
docker run -d -p 80:8000 --env-file .env network-security:latest
```

> Optionally integrate **Nginx + HTTPS** for secure traffic.

---

##  10. Experiment Tracking (DagsHub / MLflow)

* Tracks **metrics**, **parameters**, **artifacts**, and **model versions**.
* Provides a **visual dashboard** to compare multiple training runs.
* Enhances **reproducibility** and **collaboration**.

---

## 🪪 11. Logging & Troubleshooting

* **Logs** stored under `logs/` directory.
* **Custom exceptions** provide meaningful error messages.
* Common issues (MongoDB, missing model, Docker permission) are clearly logged with suggested fixes.

---

##  12. Future Enhancements

 Build model registry for versioned rollouts
 Secure API with authentication and key management
 Support canary/blue-green deployments
 Add Prometheus + Grafana dashboards

---

## 🤝 13. Contributing

* Fork the repository
* Create a feature branch
* Commit and push changes
* Submit a pull request

Please follow modular coding practices and include tests for any new features.

---


##  14. Author

**Deepak Pandey**
B.Tech – Artificial Intelligence & Machine Learning

* **GitHub:** [@28Deepakpandey](https://github.com/28Deepakpandey)
* **LinkedIn:** [Deepak Pandey](https://www.linkedin.com/in/deepak-pandey28)
