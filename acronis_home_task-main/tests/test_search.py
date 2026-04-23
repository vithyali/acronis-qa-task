#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:14:51 2026

@author: vithyali
"""

import pytest
import requests
URL = "http://localhost:8000"

#search
def test_Search():
    key = ["Nessus", "GnuTLS", "CVE-2021-44228"]
    for keywords in key:
        response = requests.get(f"{URL}/findings/search", params={"q":keywords}, timeout=10)
        if response.status_code == 200:
            print(f"{keywords} found ")
        else:
            print(f"{keywords} not found")
        assert response.status_code == 200