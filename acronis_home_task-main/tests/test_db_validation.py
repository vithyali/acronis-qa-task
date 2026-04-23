#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:16:41 2026

@author: vithyali
"""

import pytest
import requests
import psycopg2
URL = "http://localhost:8000"
def test_DataIntergrity(db_cursor):
    response = requests.get(f"{URL}/findings/", params={"page": 1,"per_page": 1})
    assert response.status_code == 200
    is_id = response.json()["items"][0]["id"]
    response_del = requests.delete(f"{URL}/findings/{is_id}")
    assert response_del.status_code == 204
    db_cursor.execute("select is_dismissed FROM findings WHERE id=%s", (is_id,))
    result = db_cursor.fetchone()
    assert result[0] is True 
    print("is_dismissed is successful")