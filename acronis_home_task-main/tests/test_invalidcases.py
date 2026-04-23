#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 17:58:04 2026

@author: vithyali
"""

import pytest
import requests
URL = "http://localhost:8000"

#READ
def test_READ():
    try:
        response_GET = requests.get(f"{URL}/findings/1231234566", timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("READ: server not connected") 
    except requests.exceptions.Timeout:
        pytest.fail("READ: system took too long to respond")
    assert response_GET.status_code == 404
    print("API STATUS CODE:", response_GET.status_code, "GET: ID not found")



#CREATE
def test_CREATE():
    
    try:
        response_POST = requests.post(f"{URL}/findings", json={}, timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("CREATE: server not connected") 
    except requests.exceptions.Timeout:
        pytest.fail("CREATE: system took too long to respond")
    assert response_POST.status_code == 422
    print("API STATUS CODE:", response_POST.status_code, "crate :Unable to process the data")

#DELETE
def test_DELETE():
    try:
        response_DELETE = requests.delete(f"{URL}/findings/-2", timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("DELETE : Server not running!")
    except requests.exceptions.Timeout:
        pytest.fail("update: Server timeout!")
    assert response_DELETE.status_code == 404
    print("API STATUS CODE:", response_DELETE.status_code, "DELETE :FINDING NOT FOUND")
