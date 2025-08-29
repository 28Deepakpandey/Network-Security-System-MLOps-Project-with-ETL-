Network Security System – End-to-End MLOps with ETL

Network Security System is a production-oriented MLOps project that detects phishing / malicious websites (network intrusion) using a full automated pipeline: data ingestion → validation → ETL/preprocessing → model training → artifact versioning → inference API → CI/CD → cloud deployment → experiment tracking.

This README is the final, complete, copy-paste-ready documentation for your GitHub repo. It includes everything a reviewer, hiring manager or fellow developer needs to understand, run, reproduce, and extend the project.

🧭 Quick links

Repo: https://github.com/28Deepakpandey/Network-Security-System-MLOps-Project-with-ETL-

Experiment tracking: https://dagshub.com/deepakpandey28july/Network-Security-System-MLOps-Project-with-ETL-/experiments

API docs (local): http://127.0.0.1:8000/docs

Contents

Project summary

Why this project

Dataset (columns & sample rows)

Architecture & pipeline (text flow)

Project structure — file/folder explanations

Setup & run (detailed)

APIs (examples)

Modeling details & artifacts

CI/CD & Deployment (GitHub Actions → ECR → EC2)

Experiment tracking (DagsHub) & reproducibility

Logging, errors & troubleshooting

Future roadmap & improvements

Contributing & license

Author / contact

Project summary

A modular, extensible MLOps system that:

Ingests network/URL features into MongoDB (push script / automated ingestion).

Validates input against schema (data_schema/schema.yaml).

Applies deterministic preprocessing (preprocessor saved).

Trains models (XGBoost used as final model; other algorithms tested).

Saves trained artifacts to final_model/ (preprocessor.pkl, model.pkl).

Exposes training and inference through a FastAPI service (app.py).

Packages with Docker and deploys via GitHub Actions to AWS ECR + EC2.

Tracks experiments and artifacts using DagsHub.

Why this project

Demonstrates MLOps best practices (modularity, reproducibility, CI/CD).

Useful for real-world deployment of network intrusion / phishing classifiers.

Combines ML engineering, backend APIs and cloud deployment end-to-end — great for portfolios and interviews.

Dataset — columns & two sample rows

Columns (30 features + target Result)

having_IP_Address, URL_Length, Shortining_Service, having_At_Symbol, double_slash_redirecting, Prefix_Suffix, having_Sub_Domain, SSLfinal_State, Domain_registeration_length, Favicon, port, HTTPS_token, Request_URL, URL_of_Anchor, Links_in_tags, SFH, Submitting_to_email, Abnormal_URL, Redirect, on_mouseover, RightClick, popUpWidnow, Iframe, age_of_domain, DNSRecord, web_traffic, Page_Rank, Google_Index, Links_pointing_to_page, Statistical_report, Result


Two example rows (as provided):

-1,1,1,1,-1,-1,-1,-1,-1,1,1,-1,1,-1,1,-1,-1,-1,0,1,1,1,1,-1,-1,-1,-1,1,1,-1,-1
1,1,1,1,1,-1,0,1,-1,1,1,-1,1,0,-1,-1,1,1,0,1,1,1,1,-1,-1,0,-1,1,1,1,-1


Result values: -1 → phishing/malicious, 1 → legitimate.

Keep your data_schema/schema.yaml in sync with these columns — ingestion & validation depend on it.

Architecture & pipeline (text flow)
Data Sources (CSV files / push_data.py)  →  MongoDB Atlas (collection)
                 ↓
         data_ingestion.py             # reads from MongoDB → pandas
                 ↓
        data_validation.py             # schema.yaml checks, null checks
                 ↓
    data_transformation.py             # cleanup, encoding, scaling
                 ↓
       model_trainer.py                # train/test split, CV, hyperparam tuning
                 ↓
        final_model/ (artifacts)       # preprocessor.pkl, model.pkl
                 ↓
             app.py (FastAPI)          # /train, /predict endpoints
                 ↓
 Dockerize (Dockerfile) → Push to ECR → Deploy on EC2
                 ↓
      Experiment tracking: DagsHub/MLflow (runs, metrics, artifacts)

Project structure — file/folder explanations

app.py — FastAPI application (endpoints: /train, /predict) and MongoDB connection.

requirements.txt — Python dependencies (FastAPI, scikit-learn, pandas, pymongo, xgboost, uvicorn, certifi, python-dotenv, etc.).

Dockerfile — Docker image build instructions for the app.

.github/workflows/ — GitHub Actions workflows for CI/CD (build, test, push image, deploy).

data_schema/schema.yaml — expected columns, dtypes and simple validation rules.

templates/table.html — Jinja2 template to render prediction DataFrame as HTML.

networksecurity/ — main package:

  components/ — data_ingestion.py, data_transformation.py, data_validation.py, model_trainer.py — modular pipeline components.
  
  pipeline/ — training_pipeline.py orchestrates components end-to-end.
  
  utils/ — main_utils and ml_utils helper functions and NetworkModel wrapper (applies preprocessor then model).
  
  logging/ — centralized logger configuration.
  
  exception/ — custom exception types to standardize error handling.
  
  cloud/ — helpers for cloud I/O (S3/ECR helpers or planned).

final_model/ — serialized artifacts: preprocessor.pkl, model.pkl.

Network_Data/ — raw or local datasets used for experimentation.

prediction_output/ — where CSV prediction outputs are written (output.csv).

push_data.py — helper to push dataset(s) into MongoDB (used for continuous ingestion).

test_mongodb.py — quick MongoDB connectivity test.

Setup & run (detailed)
Prerequisites

Python 3.9+ (3.10 recommended)

Docker (for container runs)

AWS CLI (if deploying to ECR/EC2 from your machine)

MongoDB Atlas account + cluster (or local MongoDB)

Steps

Clone

git clone https://github.com/28Deepakpandey/Network-Security.git
cd Network-Security


Create & activate venv

python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate


Install dependencies

pip install -r requirements.txt


Create .env

MONGODB_URL_KEY="mongodb+srv://<user>:<password>@<cluster>/<db>?retryWrites=true&w=majority"


Use certifi CA if needed (code already imports and uses ca = certifi.where() for tlsCAFile).

(Optional) Push dataset to MongoDB

python push_data.py   # ensure push_data.py points to your CSV and uses MONGODB_URL_KEY


Run training locally

Via script (recommended for development)

python main.py        # triggers training pipeline (same as visit /train)


Or via API

# Start API server
python app.py             # runs Uvicorn server: 0.0.0.0:8000
# Then call
GET http://127.0.0.1:8000/train


Make predictions

Use Swagger UI: http://127.0.0.1:8000/docs → POST /predict → upload CSV.

Or curl:

curl -X POST "http://127.0.0.1:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@Network_Data/phisingData.csv"


Results saved to prediction_output/output.csv and rendered as HTML (table).

APIs (detailed examples)
Start server
python app.py
# or
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

Trigger training

Request

GET /train


Behavior

Orchestrates full pipeline and saves artifacts into final_model/.

Returns Training is successful (or raises structured exception).

Predict on CSV

Request

POST /predict
Form-data: file (CSV)


Behavior

Reads CSV into DataFrame.

Loads final_model/preprocessor.pkl and final_model/model.pkl.

Runs NetworkModel wrapper to preprocess and predict.

Adds predicted_column to DataFrame.

Writes prediction_output/output.csv.

Renders HTML table via templates/table.html.

Note: If you prefer JSON output for API consumers, you can modify the endpoint to return {"predictions": [..]} — currently the route renders HTML.

Modeling details & artifacts

Preprocessing

Implemented within data_transformation.py. Typical steps:

Column selection

Encoding categorical features (OneHot/Label where required)

Scaling numeric features (StandardScaler / MinMax)

Missing value handling

Preprocessor saved to final_model/preprocessor.pkl.

Models tried

Logistic Regression, Random Forest, XGBoost.

Final model: XGBoost (selected for balanced performance & speed). Hyperparameters tuned via GridSearchCV / cross-validation when appropriate.

Evaluation

Metrics logged per run: Accuracy, Precision, Recall, F1, ROC-AUC.

Evaluation artifacts stored and visible in DagsHub experiments.

Serialization

pickle / joblib used to persist preprocessor.pkl and model.pkl into final_model/.

If you add very large models or many artifacts, consider a model registry or object storage (S3/ECR/Git LFS/DagsHub artifacts).

CI/CD & Deployment (GitHub Actions → ECR → EC2)
Recommended high-level workflow

On push to main:

Checkout code

Run quick tests/lint (if present)

Build Docker image (docker build)

Authenticate to AWS ECR (aws ecr get-login-password)

Tag & push image to ECR

SSH to EC2 (or use self-hosted runner) and docker pull + docker run (replace old container)

GitHub Secrets (set in repo Settings → Secrets)

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_REGION

ECR_REPOSITORY (e.g., network-security)

EC2_HOST (public IP)

EC2_USER (ubuntu / ec2-user)

EC2_SSH_KEY (private key, or use Actions deploy keys)

ECR push example (local)
# Authenticate
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com

# Build
docker build -t network-security:latest .

# Tag
docker tag network-security:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/network-security:latest

# Push
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/network-security:latest

EC2 run example (on EC2)
docker pull <aws_account_id>.dkr.ecr.<region>.amazonaws.com/network-security:latest
docker stop network-security || true
docker rm network-security || true
docker run -d --name network-security -p 80:8000 --env-file /home/ubuntu/.env <aws_account_id>.dkr.ecr.<region>.amazonaws.com/network-security:latest


Consider using a reverse proxy (Nginx) for port 80/443 and certificates (Let's Encrypt) for secure traffic.

Experiment tracking — DagsHub / MLflow

Training runs log:

Hyperparameters

Metrics (Accuracy, F1, ROC-AUC)

Artifacts (preprocessor, model)

DagsHub provides an online UI to compare runs, diff params and download artifacts. Link in top of README.

Tip: Save a run_id inside artifacts/metadata so you can map artifacts → experiment run.

Logging, errors & troubleshooting
Logging

Centralized logger configured in networksecurity/logging/logger.py. Logs are written to logs/ (configurable).

Common issues & quick fixes

MongoDB connection error

Check MONGODB_URL_KEY in .env.

Whitelist your IP in MongoDB Atlas Network Access.

Ensure TLS/CA certs are available (code uses certifi.where()).

Model file missing

Run GET /train or python main.py to generate final_model/model.pkl and preprocessor.pkl.

Port 8000 already in use

Kill the process using that port, or change host/port in app.py/Uvicorn command.

Docker permission errors

On EC2, add your user to docker group or use sudo to run Docker commands.

CI/CD failures

Check action logs on GitHub Actions tab. Ensure AWS secrets are set and ECR repository exists.

Future roadmap & improvements

Add unit tests and integrate into CI stage.

Add model monitoring & drift detection (Prometheus + Grafana + custom drift checks).

Add blue/green or canary deploys for model rollout safety.

Implement model registry and versioned deployments (MLflow model registry / DagsHub artifacts).

Replace hardcoded file paths with configurable Config object / CLI params.

Add auth for API endpoints and secure secrets in a secrets manager (AWS Secrets Manager).

Contributing & license
Contributing

Open an issue to discuss major changes.

Fork the repo → feature branch → PR.

Keep commits small and PRs focused.

Add unit tests for new functionality.

License

This repo uses MIT License (add LICENSE file in repo root).

👨‍💻 Author

Deepak Pandey
B.Tech – Artificial Intelligence & Machine Learning

🌐 GitHub
 | LinkedIn
