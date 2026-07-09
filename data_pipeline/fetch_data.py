import requests
import pandas as pd
import datetime
import random
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

def fetch_clinical_trials(status="TERMINATED", max_records=100):
    """
    Fetches clinical trials data using ClinicalTrials.gov API v2.
    We are looking for trials that were terminated.
    """
    print(f"Fetching {max_records} {status} clinical trials...")
    
    # Using ClinicalTrials.gov API v2
    url = f"https://clinicaltrials.gov/api/v2/studies?query.term={status}&pageSize={max_records}"
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch data from ClinicalTrials.gov API")
        return []

    data = response.json()
    studies = data.get("studies", [])
    
    processed_trials = []
    
    for study in studies:
        protocol = study.get("protocolSection", {})
        ident = protocol.get("identificationModule", {})
        status_mod = protocol.get("statusModule", {})
        interventions_mod = protocol.get("armsInterventionsModule", {})
        
        nct_id = ident.get("nctId", "UNKNOWN")
        title = ident.get("briefTitle", "UNKNOWN")
        why_stopped = status_mod.get("whyStopped", "Reason not provided")
        completion_date = status_mod.get("completionDateStruct", {}).get("date", "UNKNOWN")
        
        # Try to find interventions/drugs
        drugs = []
        if "interventions" in interventions_mod:
            for inv in interventions_mod["interventions"]:
                if inv.get("type") == "DRUG":
                    drugs.append(inv.get("name"))
                    
        drug_name = drugs[0] if drugs else "Unknown Drug"
        
        processed_trials.append({
            "nct_id": nct_id,
            "title": title,
            "drug_name": drug_name,
            "termination_date": completion_date,
            "termination_reason": why_stopped
        })
        
    df = pd.DataFrame(processed_trials)
    df.to_csv('data/clinical_trials_terminated.csv', index=False)
    print(f"Saved {len(df)} trials to data/clinical_trials_terminated.csv")
    return df

def generate_shortage_labels(trials_df):
    """
    Because FDA Drug Shortage data doesn't have a clean, easy-to-use API 
    that maps 1:1 with ClinicalTrials drug names for a quick MVP,
    we generate synthetic shortage labels based on the clinical trial data 
    to demonstrate the Machine Learning pipeline.
    
    Hypothesis: Certain termination reasons correlate with future shortages.
    """
    print("Generating correlation labels for Machine Learning Model...")
    
    def simulate_shortage(row):
        # We simulate the hypothesis: 
        # If a trial is terminated due to "manufacturing", "supply", or "funding", 
        # there is a higher probability of a drug shortage 3-18 months later.
        reason = str(row['termination_reason']).lower()
        
        high_risk_keywords = ['manufactur', 'supply', 'funding', 'safety', 'efficacy']
        is_high_risk = any(keyword in reason for keyword in high_risk_keywords)
        
        if is_high_risk:
            # 70% chance of shortage if high risk
            shortage_occurs = random.random() < 0.70
        else:
            # 20% baseline chance of shortage
            shortage_occurs = random.random() < 0.20
            
        # If shortage occurs, simulate the gap in months (3 to 18)
        months_to_shortage = random.randint(3, 18) if shortage_occurs else -1
        
        return pd.Series([int(shortage_occurs), months_to_shortage])
    
    trials_df[['shortage_occurred', 'months_to_shortage']] = trials_df.apply(simulate_shortage, axis=1)
    
    trials_df.to_csv('data/training_data.csv', index=False)
    print("Saved training dataset to data/training_data.csv")
    return trials_df

if __name__ == "__main__":
    df = fetch_clinical_trials(max_records=200)
    if not df.empty:
        generate_shortage_labels(df)
        print("Data Pipeline Completed Successfully!")
