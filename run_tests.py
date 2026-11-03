#!/usr/bin/env python3
"""
DRUG SHORTAGE PREDICTOR — Automated Verification Suite Runner
Ensures model weights exist, runs training if missing, and executes unit tests.
"""

import sys
import os
import unittest

def run_suite():
    print("=" * 70)
    print("RUNNING DRUG SHORTAGE PREDICTOR VERIFICATION SUITE")
    print("=" * 70)
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, root_dir)
    
    model_path = os.path.join(root_dir, "ai_model", "shortage_model.pkl")
    if not os.path.exists(model_path):
        print("[INFO] Model weights not found. Running ai_model/train.py...")
        from ai_model.train import train_model
        train_model()
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.join(root_dir, "tests"), pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 70)
    print("VERIFICATION SUITE COMPLETED")
    print(f"Total Tests Run: {result.testsRun} | Passed: {result.testsRun - len(result.failures) - len(result.errors)} | Failed: {len(result.failures) + len(result.errors)}")
    
    if result.wasSuccessful():
        print("Overall Result: SUCCESS [All Pipeline Components Verified]")
        print("=" * 70)
        return 0
    else:
        print("Overall Result: FAILED")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(run_suite())
