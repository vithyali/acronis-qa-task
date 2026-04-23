#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:50:14 2026

@author: vithyali
"""
import pytest
import requests
import psycopg2
def test_findings_asset_consistency(db_cursor):
    db_cursor.execute("SELECT f.id, f.asset_id FROM findings f LEFT JOIN assets a ON f.asset_id = a.id WHERE a.id IS NULL")
    entity = db_cursor.fetchall()

    if len(entity) == 0:
        print("All findings have valid asset")
    else:
        for row in entity:
            print("Finding id", row[0], "points to missing asset_id", row[1])

    assert len(entity) == 0, f"Found {len(entity)} findings with no matching asset: {entity}"


def test_findings_vulnerability_consistency(db_cursor):
    db_cursor.execute("""
        SELECT f.id, f.vulnerability_id
        FROM findings f
        LEFT JOIN vulnerabilities v ON f.vulnerability_id = v.id
        WHERE v.id IS NULL
    """)
    entity_v = db_cursor.fetchall()

    if len(entity_v) == 0:
        print("All findings have valid vulnerability")
    else:
        for row in  entity_v:
            print("Finding id", row[0], "points to missing vulnerability_id", row[1])

    assert len( entity_v) == 0, f"Found {len( entity_v)} findings with no matching vulnerability: { entity_v}"