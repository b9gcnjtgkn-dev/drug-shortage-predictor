# 🏥 Drug Shortage Predictor AI

**Predicting FDA injectable drug shortage onset 3–18 months in advance from ClinicalTrials.gov termination signals.**

An end-to-end Machine Learning web application designed to investigate if linguistic signals in clinical trial terminations can act as an early-warning radar for systemic pharmaceutical supply chain failures.

---

## 🔬 The Research Question

*Can clinical trial termination signals from ClinicalTrials.gov predict FDA injectable drug shortage onset 3–18 months in advance, before shortages become operationally visible?*

Historically, drug shortages are only detected *after* they hit the market. This project hypothesizes that when a clinical trial is terminated due to reasons like **manufacturing deviations**, **loss of funding**, or **severe safety events**, these serve as "canary in the coal mine" signals that the underlying sponsor or manufacturing facility is compromised, which will eventually cascade into a physical drug shortage months later.

---

## 🏗️ Architecture & Tech Stack

This project is structured as a monorepo containing a full-stack AI product:

1. **Data Pipeline (Python)**
   - Automatically connects to the **ClinicalTrials.gov API (v2)**.
   - Fetches historical data on terminated trials for injectable drugs, parsing out the explicit reasons for termination.
2. **AI / ML Model (Python, scikit-learn)**
   - Uses Natural Language Processing (TF-IDF) to analyze the text of trial termination reasons.
   - A Random Forest Classifier trained to predict the probability of a shortage occurring 3-18 months later based on high-risk signal detection.
3. **Backend API (FastAPI)**
   - High-performance API server that loads the trained `.pkl` ML model and exposes real-time prediction endpoints.
4. **Frontend Dashboard (Next.js, React)**
   - A beautiful, modern Glassmorphism UI allowing users to test the AI model in real-time and visualize the historical training data.

---

## 🚀 Quick Start (Local Setup)

Follow these steps to run the complete AI product on your local machine (Mac).

### 1. Prerequisites
Ensure you have the following installed. If you are on a Mac, you can run the provided setup script:
```bash
# This will install Homebrew, Python 3.11, and Node.js
bash setup_mac.sh
```

### 2. Run the Application
The project includes a master script that automatically launches both the Python Backend and the Next.js Frontend concurrently.

```bash
# Make the script executable (only needed once)
chmod +x start.sh

# Start the servers!
./start.sh
```

### 3. View the Dashboard
Once the servers start, open your web browser and navigate to:
**http://localhost:3000**

---

## 🧪 Testing the Model

To see the AI in action, open the dashboard at `localhost:3000` and paste these test cases into the termination reason box:

* **High Risk Example (Supply Chain Failure):**
  > *"The sponsor decided to terminate the trial early due to severe manufacturing deviations at the primary API facility, resulting in a compromised supply of the investigational product."*
  
* **Low Risk Example (Logistical/Recruitment Failure):**
  > *"The clinical trial was terminated prematurely because of poor patient recruitment and slow enrollment rates at multiple international sites. No patient risk was identified."*

---

## 📂 Project Structure

```text
drug-shortage-predictor/
├── data_pipeline/         # Scripts fetching from ClinicalTrials.gov API
├── ai_model/              # Random Forest training scripts and exported .pkl models
├── backend/               # FastAPI application
├── frontend/              # Next.js web application
├── data/                  # Generated CSV datasets
├── start.sh               # Master script to run both servers
└── setup_mac.sh           # Environment bootstrapping script
```
