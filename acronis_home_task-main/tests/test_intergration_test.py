#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 12:12:42 2026

@author: vithyali
"""

import pytest
import requests
import psycopg2

scan_URL = "http://localhost:8001/scans"
dashboard_URL = "http://localhost:8000/findings"
scan_id = None
#CREATE SCAN ID AND ADD IT TO DB
def test_createScanID(db_cursor):
    global scan_id
    #COUNT DASHBOARD ID BEFORE SCANNING
    responseDashboard = requests.get(f"{dashboard_URL}", timeout=10) 
    assert responseDashboard.status_code == 200
    data = responseDashboard.json()
    currentFindings_count = data["total"]
    
    #ADD PAYLOAD/SCANNING OPERATON
    payload = {"asset_id": 1, "scanner_name": "Qualys", "vulnerability_ids": [1,7,8]}
    responseScan = requests.post(f"{scan_URL}", json = payload, timeout =10)
    assert responseScan.status_code == 201
    scan_id = responseScan.json()["id"]  
    
    #COUNTDASHBOARD ID AFTER SCANNING  
    responseDashboard = requests.get(f"{dashboard_URL}", timeout=10) 
    assert responseDashboard.status_code == 200
    data = responseDashboard.json()
    afterScanFindings_count = data["total"]   
    
    #COMPARISON 
    
    assert currentFindings_count < afterScanFindings_count, ( 
        "No new scan id added"
        )
    print(f"New scan id added succesfully and the ID is:,{scan_id}")
#UPDATE STATUS IN     
def test_status_update_reflects_in_db(db_cursor):
    res = requests.get(f"{dashboard_URL}", timeout=10)
    valid_id = res.json()["items"][0]["id"]
    payload = {"status": "confirmed", "notes": "integration test"}
    response = requests.put(f"{dashboard_URL}/{valid_id}/status", json=payload, timeout=10)
    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"

    db_cursor.execute("SELECT status FROM findings WHERE id = %s", (valid_id,))
    result = db_cursor.fetchone()
    assert result[0] == "confirmed", f"DB not updated — got {result[0]}"
    
     
    

        