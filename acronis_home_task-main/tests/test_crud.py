#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 17:25:47 2026

@author: vithyali
"""

import pytest
import requests
URL = "http://localhost:8000"
new_id = None

#READ
def test_READ():
    response_GET = requests.get(f"{URL}/findings")
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
    response_POST =  requests.post(f"{URL}/findings", json=payload)
    assert response_POST.status_code == 201
    assert response_POST.json()["status"] == "open"
    new_id = response_POST.json()["id"]

#UPDATE 
def test_UPDATE():
    payload = {"status": "confirmed","notes": "hello"}
    response_PUT = requests.put(f"{URL}/findings/{new_id}/status", json=payload)
    assert response_PUT.status_code == 200
    assert response_PUT.json()["status"] == "confirmed"

#DELETE
def test_DELETE():
    response_DELETE = requests.delete(f"{URL}/findings/{new_id}")
    assert response_DELETE.status_code == 204
    
    
#VULNERABILITIES
def test_vulnerabilities_list():
    response = requests.get(f"{URL}/vulnerabilities", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))
