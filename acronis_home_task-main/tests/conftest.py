#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:36:57 2026

@author: vithyali
"""

import pytest
import psycopg2

@pytest.fixture(scope="session")
def db():
    conn = psycopg2.connect(
        host="localhost",
        port=5433,
        dbname="qa_test",
        user="qa_user",
        password="qa_password"
    )
    yield conn
    conn.close()

@pytest.fixture(scope="session")
def db_cursor(db):
    cursor = db.cursor()
    yield cursor
    cursor.close()