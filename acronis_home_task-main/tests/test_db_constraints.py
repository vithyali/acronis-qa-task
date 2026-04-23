#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:14:47 2026

@author: vithyali
"""
import pytest
import requests
import psycopg2
URL = "http://localhost:8000"
def test_DataIntergrity(db_cursor):
    db_cursor.execute("select id, cvss_score FROM vulnerabilities WHERE  cvss_score < 0 OR  cvss_score > 10")
    not_valid = db_cursor.fetchall()
    if len(not_valid) == 0:
        print("all cvss inputs are valid")
    else:
        for tuple_row in not_valid:    
            print("Following ids", tuple_row[0], "has violation", tuple_row[1])
    assert len(not_valid) == 0
    db_cursor.execute("SELECT id FROM findings WHERE asset_id IS NULL OR    vulnerability_id IS NULL OR status IS NULL OR detected_at IS NULL")
    null_rows = db_cursor.fetchall()
    if len(null_rows) == 0:
        print("None of the rows have empty values")
    else:
        for ii in null_rows:
            print(ii[0] ,"id has null values")
    assert len(null_rows) == 0