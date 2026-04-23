#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:50:40 2026

@author: vithyali
"""
import pytest
import requests
from playwright.sync_api import sync_playwright

URL ="http://localhost:8000"
def test_run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)
        page.wait_for_load_state("networkidle")
        assert page.title() != "","page did not load"
        print(page.title(), "page loaded sucessfully")
        #CHECK FINDINGS AVIALABLABLITY
        assert page.locator("table").first.is_visible(), "Findings table not visible"
        rows = page.locator("table").first.locator("tbody tr")
        assert rows.count() > 0, "No findings found in table"
        print(f"Dashboard loaded with {rows.count()} findings")
        browser.close()


def test_change_finding_status():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)
        page.wait_for_load_state("networkidle")
        #CHANGING THE STATUS OF FINDING USING DROPDOWN
        dropdown = page.locator("select").first
        dropdown.wait_for(state="visible", timeout=30000)
        dropdown.select_option("confirmed")
        page.wait_for_timeout(1000)
        # NEW VALUE IN DROPDOWN VERIFICATION
        selected = dropdown.input_value()
        assert selected == "confirmed", f"Status not updated : got {selected}"
        print("Status changed to confirmed successfully")
        browser.close()