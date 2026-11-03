"""
DRUG SHORTAGE PREDICTOR — Comprehensive Verification Suite
Tests data pipeline integrity, TF-IDF NLP model inference, FastAPI endpoints, and edge cases.
"""

import unittest
import os
import sys
import pickle
import pandas as pd

# Ensure root directory is on PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app, predict_shortage, get_historical_data, PredictionRequest


class TestDrugShortagePredictor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.data_path = os.path.join(cls.base_dir, "data", "training_data.csv")
        cls.model_path = os.path.join(cls.base_dir, "ai_model", "shortage_model.pkl")
        cls.vec_path = os.path.join(cls.base_dir, "ai_model", "vectorizer.pkl")

    # Test 1: Training Dataset Schema and Completeness
    def test_training_data_schema(self):
        self.assertTrue(os.path.exists(self.data_path), "training_data.csv must exist.")
        df = pd.read_csv(self.data_path)
        self.assertGreater(len(df), 0, "Dataset must not be empty.")
        expected_cols = {"nct_id", "title", "drug_name", "termination_reason", "shortage_occurred"}
        for col in expected_cols:
            self.assertIn(col, df.columns, f"Missing required column: {col}")

    # Test 2: AI Model and Vectorizer Artifact Verification
    def test_model_and_vectorizer_artifacts(self):
        self.assertTrue(os.path.exists(self.model_path), "shortage_model.pkl must exist.")
        self.assertTrue(os.path.exists(self.vec_path), "vectorizer.pkl must exist.")
        
        with open(self.model_path, "rb") as f:
            model = pickle.load(f)
        with open(self.vec_path, "rb") as f:
            vectorizer = pickle.load(f)
            
        self.assertIsNotNone(model)
        self.assertIsNotNone(vectorizer)

    # Test 3: Model Inference & Probability Calibration
    def test_prediction_inference(self):
        req = PredictionRequest(
            termination_reason="Sponsor terminated study due to manufacturing facility non-compliance and drug shortage."
        )
        res = predict_shortage(req)
        
        self.assertIn("termination_reason", res)
        self.assertIn("shortage_risk_probability", res)
        self.assertIn("high_risk", res)
        self.assertIsInstance(res["high_risk"], bool)
        self.assertGreaterEqual(float(res["shortage_risk_probability"]), 0.0)
        self.assertLessEqual(float(res["shortage_risk_probability"]), 1.0)

    # Test 4: Low-Risk / Non-Supply Termination Handling
    def test_low_risk_termination_reason(self):
        req = PredictionRequest(
            termination_reason="Trial completed successfully as per protocol with all endpoints met."
        )
        res = predict_shortage(req)
        self.assertEqual(res["high_risk"], False)
        self.assertLess(float(res["shortage_risk_probability"]), 0.50)

    # Test 5: Root API Health Check Endpoint
    def test_api_root_endpoint(self):
        from backend.main import read_root
        response = read_root()
        self.assertIn("message", response)
        self.assertIn("running", response["message"].lower())

    # Test 6: Historical Data Retrieval Endpoint
    def test_historical_data_endpoint(self):
        res = get_historical_data(limit=10)
        self.assertIn("data", res)
        self.assertEqual(len(res["data"]), 10)
        first_row = res["data"][0]
        self.assertIn("nct_id", first_row)
        self.assertIn("drug_name", first_row)


if __name__ == "__main__":
    unittest.main()
