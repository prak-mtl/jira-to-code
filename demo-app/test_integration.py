#!/usr/bin/env python3
"""
Integration test script to verify backend API endpoints
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    assert response.status_code == 200
    print("  ✅ PASSED\n")

def test_root():
    """Test root endpoint"""
    print("Testing / endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    assert response.status_code == 200
    print("  ✅ PASSED\n")

def test_commit_frequency():
    """Test commit frequency endpoint"""
    print("Testing /metrics/commit_frequency endpoint...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    params = {
        "team_id": "demo-team",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }
    
    response = requests.get(f"{BASE_URL}/metrics/commit_frequency", params=params)
    print(f"  Status: {response.status_code}")
    data = response.json()
    print(f"  Response: {len(data)} days of data")
    if data:
        print(f"  Sample: {data[0]}")
    assert response.status_code == 200
    assert isinstance(data, list)
    print("  ✅ PASSED\n")

def test_pr_analytics():
    """Test PR analytics endpoint"""
    print("Testing /metrics/pr_analytics endpoint...")
    
    params = {"team_id": "demo-team"}
    
    response = requests.get(f"{BASE_URL}/metrics/pr_analytics", params=params)
    print(f"  Status: {response.status_code}")
    data = response.json()
    print(f"  Response: {json.dumps(data, indent=2)}")
    assert response.status_code == 200
    assert "total_prs" in data
    assert "merged_prs" in data
    print("  ✅ PASSED\n")

def test_pr_velocity():
    """Test PR velocity endpoint"""
    print("Testing /metrics/pr_velocity endpoint...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    params = {
        "team_id": "demo-team",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }
    
    response = requests.get(f"{BASE_URL}/metrics/pr_velocity", params=params)
    print(f"  Status: {response.status_code}")
    data = response.json()
    print(f"  Response: {json.dumps(data, indent=2)}")
    assert response.status_code == 200
    assert "value" in data
    print("  ✅ PASSED\n")

def main():
    print("=" * 60)
    print("Backend API Integration Tests")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_root()
        test_commit_frequency()
        test_pr_analytics()
        test_pr_velocity()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to backend at", BASE_URL)
        print("Make sure the backend is running: cd demo-app/backend && python simple_main.py")
        return 1
    except AssertionError as e:
        print(f"❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

