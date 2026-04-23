#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 17:47:43 2026

@author: vithyali
"""
import pytest
import requests
URL = "http://localhost:8000"
SCANNER_URL = "http://localhost:8001"
new_id = None

#READ
def test_READ():
    try:
        response_GET = requests.get(f"{URL}/findings", timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("READ: server not connected") 
    except requests.exceptions.Timeout:
        pytest.fail("READ: system took too long to respond")
    assert response_GET.status_code == 200
    assert isinstance(response_GET.json(),dict)
    data = response_GET.json() 
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"],list)
    print("API STATUS CODE:", response_GET.status_code)

#CREATE
def test_CREATE():
    global new_id
    payload = {
      "asset_id": 1,
      "vulnerability_id": 1,
      "scanner": "Test123",
      "notes": "API TEST TASK"
    }
    try:
        response_POST = requests.post(f"{URL}/findings", json=payload, timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("CREATE: server not connected") 
    except requests.exceptions.Timeout:
        pytest.fail("CREATE: system took too long to respond")
    assert response_POST.status_code == 201
    assert response_POST.json()["status"] == "open"
    new_id = response_POST.json()["id"]

#UPDATE 
def test_UPDATE():
    payload = {"status": "confirmed","notes": "hello"}
    try:
        response_PUT = requests.put(f"{URL}/findings/{new_id}/status", json=payload, timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("update : Server not running!")
    except requests.exceptions.Timeout:
        pytest.fail("UPDATE: Server timeout!")
    assert response_PUT.status_code == 200
    assert response_PUT.json()["status"] == "confirmed"

#DELETE
def test_DELETE():
    try:
        response_DELETE = requests.delete(f"{URL}/findings/{new_id}", timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("DELETE : Server not running!")
    except requests.exceptions.Timeout:
        pytest.fail("update: Server timeout!")
    assert response_DELETE.status_code == 204
    
#HEALTH CHECKS

def test_health_dashboard():
    response = requests.get(f"{URL}/health", timeout=10)
    assert response.status_code == 200


def test_health_scanner():
    response = requests.get(f"{SCANNER_URL}/health", timeout=10)
    assert response.status_code == 200
