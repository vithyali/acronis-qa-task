#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 17:59:56 2026

@author: vithyali
"""

import pytest
import requests
URL = "http://localhost:8000"
SCANNER_URL = "http://localhost:8001"

#READ
def test_READ():
    try:
        response_GET = requests.get(f"{URL}/findings", timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("READ: server not connected") 
    except requests.exceptions.Timeout:
        pytest.fail("READ: system took too long to respond")
    #Status code validation
    assert response_GET.status_code == 200
    assert isinstance(response_GET.json(),dict)
    #Response Structure 
    #Outer Structure
    data = response_GET.json() 
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "per_page" in data
    assert isinstance(data["items"],list)
    #Inner Structure
    for inn_data in data["items"]:
        assert "id" in inn_data
        assert "asset_id" in inn_data
        assert "vulnerability_id" in inn_data
        assert "status" in inn_data
        assert "detected_at" in inn_data
        assert "resolved_at" in inn_data
        assert "scanner" in inn_data
        assert "notes" in inn_data
        assert "is_dismissed" in inn_data
    
    print("API STATUS CODE:", response_GET.status_code)
    #DATA CORRECTNESS
    #OUTER DATA CORRECTNESS
    assert isinstance(data["total"], int)       
    assert isinstance(data["page"], int)        
    assert isinstance(data["per_page"], int)
    assert data["total"] >= 0
    assert data["page"]  >= 1
    #INNER DATA CORRECTNESS
    for inn_data in data["items"]:
        assert isinstance(inn_data["id"], int)
        assert isinstance(inn_data["status"], str)
        assert isinstance(inn_data["is_dismissed"], bool)
        print("dataid is:", inn_data["id"])
        
        #FILTERS

def test_filter_by_status():
    response = requests.get(f"{URL}/findings", params={"status": "open"}, timeout=10)
    assert response.status_code == 200
    for item in response.json()["items"]:
        assert item["status"] == "open"


def test_filter_by_severity():
    response = requests.get(f"{URL}/findings", params={"severity": "critical"}, timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


def test_filter_by_asset_id():
    response = requests.get(f"{URL}/findings", params={"asset_id": 1}, timeout=10)
    assert response.status_code == 200
    for item in response.json()["items"]:
        assert item["asset_id"] == 1
        
        
        #STATS

def test_stats_risk_score():
    response = requests.get(f"{URL}/stats/risk-score", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data


def test_stats_summary():
    response = requests.get(f"{URL}/stats/summary", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert "total" in data or "by_status" in data or "by_severity" in data