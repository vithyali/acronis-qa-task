# QA Automation Engineer — Technical Assessment

**Duration:** 7 days
**Language:** Python

---

## Overview

You are given a running **Vulnerability Management Dashboard** composed of two microservices and a PostgreSQL database. The system tracks security vulnerabilities detected across your organization's assets (servers, containers, applications).

Your task is to write automated tests that verify the system works correctly — and find any bugs.

The system is already running via Docker. You don't need to modify the application code.

---

## System Architecture

```
┌──────────────┐      ┌───────────────────┐      ┌────────────────────┐
│  Dashboard UI │─────▶│  Dashboard API     │      │  Scanner Service    │
│  localhost/   │      │  localhost:8000    │      │  localhost:8001     │
└──────────────┘      └────────┬──────────┘      └──────────┬─────────┘
                               │                             │
                           ┌───▼─────────────────────────────▼───┐
                           │           PostgreSQL                 │
                           │     localhost:5433 / qa_test         │
                           └─────────────────────────────────────┘
```

---

## Connection Details

| Service            | URL / Connection                                  |
|--------------------|---------------------------------------------------|
| Dashboard API      | `http://localhost:8000`                            |
| Scanner Service    | `http://localhost:8001`                            |
| Dashboard UI       | `http://localhost:8000/`                           |
| PostgreSQL         | Host: `localhost`, Port: `5433`, DB: `qa_test`, User: `qa_user`, Password: `qa_password` |

---

## API Reference

### Scanner Service (port 8001)

Manages assets and scan operations.

| Method | Endpoint               | Description                              |
|--------|------------------------|------------------------------------------|
| GET    | `/assets`              | List assets (paginated)                  |
| GET    | `/assets/{id}`         | Get a single asset                       |
| POST   | `/assets`              | Create an asset                          |
| PUT    | `/assets/{id}`         | Update an asset                          |
| DELETE | `/assets/{id}`         | Deactivate an asset                      |
| POST   | `/scans`               | Run a scan (creates findings)            |
| GET    | `/scans`               | List scans                               |
| GET    | `/scans/{id}`          | Get scan details                         |
| GET    | `/health`              | Health check                             |

**Pagination params:** `?page=1&per_page=10`
**Filter params (assets):** `?environment=production&asset_type=server`

**Create asset payload:**
```json
{
  "hostname": "web-server-03",
  "ip_address": "10.0.1.50",
  "asset_type": "server",
  "environment": "production",
  "os": "Ubuntu 22.04"
}
```

**Run scan payload:**
```json
{
  "asset_id": 1,
  "scanner_name": "Nessus",
  "vulnerability_ids": [1, 3, 5]
}
```

### Dashboard API (port 8000)

Manages findings lifecycle, statistics, and serves the UI.

| Method | Endpoint                     | Description                              |
|--------|------------------------------|------------------------------------------|
| GET    | `/findings`                  | List findings (paginated, filterable)    |
| GET    | `/findings/{id}`             | Get finding detail with CVE info         |
| POST   | `/findings`                  | Create a finding manually                |
| PUT    | `/findings/{id}/status`      | Update finding status                    |
| DELETE | `/findings/{id}`             | Dismiss a finding                        |
| GET    | `/findings/search?q=`        | Search findings by CVE, hostname, notes  |
| GET    | `/stats/risk-score`          | Calculate overall risk score             |
| GET    | `/stats/summary`             | Summary counts by status and severity    |
| GET    | `/vulnerabilities`           | List vulnerability catalog               |
| GET    | `/vulnerabilities/{id}`      | Get vulnerability detail                 |
| GET    | `/health`                    | Health check                             |

**Filter params (findings):** `?status=open&severity=critical&asset_id=1`

**Create finding payload:**
```json
{
  "asset_id": 1,
  "vulnerability_id": 3,
  "scanner": "Nessus",
  "notes": "Detected during routine scan"
}
```

**Update status payload:**
```json
{"status": "confirmed", "notes": "Verified by security team"}
```

Valid statuses: `open`, `confirmed`, `in_progress`, `resolved`, `false_positive`

### Database Schema

```sql
assets:           id, hostname, ip_address, asset_type, environment, os, is_active, created_at
vulnerabilities:  id, cve_id, title, description, severity, cvss_score, published_date, created_at
findings:         id, asset_id, vulnerability_id, status, detected_at, resolved_at, scanner, notes, is_dismissed
scans:            id, asset_id, scanner_name, status, started_at, completed_at, findings_count
```

---

## Your Tasks

### Part 1 — API Testing
Write pytest-based tests for the **Dashboard API**:
- Findings CRUD operations (create, read, update status, dismiss)

import pytest
import requests
URL = "http://localhost:8000"

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
payload = {
  "asset_id": 78,
  "vulnerability_id": 78,
  "scanner": "Test123",
  "notes": "API TEST TASK"
}
response_POST =  requests.post(f"{URL}/findings", json=payload)
assert response_POST.status_code == 201
assert response_POST.json()["status"] == "open"

#UPDATE 
def test_UPDATE():
payload = {"status": "confirmed","vulnerability_id": 12}
response_PUT = requests.put(f"{URL}/findings/2", json=payload)
assert response_PUT.status_code == 200
assert response_PUT.json()["status"] == "confirmed"

#DELETE
def test_DELETE():
response_DELETE = requests.delete(f"{URL}/findings/2")
assert response_DELETE.status_code == 200





- Error handling (invalid inputs, non-existent resources)

import pytest
import requests
URL = "http://localhost:8000"

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
    payload = {
      "asset_id": 78,
      "vulnerability_id": 78,
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

#UPDATE 
def test_UPDATE():
    payload = {"status": "confirmed","vulnerability_id": 12}
    try:
        response_PUT = requests.put(f"{URL}/findings/2", json=payload, timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("update : Server not running!")
    except requests.exceptions.Timeout:
        pytest.fail("UPDATE: Server timeout!")
    assert response_PUT.status_code == 200
    assert response_PUT.json()["status"] == "confirmed"

#DELETE
def test_DELETE():
    try:
        response_DELETE = requests.delete(f"{URL}/findings/2", timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("DELETE : Server not running!")
    except requests.exceptions.Timeout:
        pytest.fail("update: Server timeout!")
    assert response_DELETE.status_code == 200


- Edge cases (invalid status values, boundary values)

#Negative cases examples 

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

- Validate response status codes, response structure, and data correctness

import pytest
import requests
URL = "http://localhost:8000"

#READ
def test_READ():
    try:
        response_GET = requests.get(f"{URL}/findings", timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("READ: server not connected") 
    except requests.exceptions.Timeout:
        pytest.fail("READ: system took too long to respond")
    #Status code validation
    assert response_GET.status_code == 200
    assert isinstance(response_GET.json(),dict)
    #Response Structure 
    #Outer Structure
    data = response_GET.json() 
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "per_page" in data
    assert isinstance(data["items"],list)
    #Inner Structure
    for inn_data in data["items"]:
        assert "id" in inn_data
        assert "asset_id" in inn_data
        assert "vulnerability_id" in inn_data
        assert "status" in inn_data
        assert "detected_at" in inn_data
        assert "resolved_at" in inn_data
        assert "scanner" in inn_data
        assert "notes" in inn_data
        assert "is_dismissed" in inn_data
    
    print("API STATUS CODE:", response_GET.status_code)
    #DATA CORRECTNESS
    #OUTER DATA CORRECTNESS
    assert isinstance(data["total"], int)       
    assert isinstance(data["page"], int)        
    assert isinstance(data["per_page"], int)
    assert data["total"] >= 0
    assert data["page"]  >= 1
    #INNER DATA CORRECTNESS
    for inn_data in data["items"]:
        assert isinstance(inn_data["id"], int)
        assert isinstance(inn_data["status"], str)
        assert isinstance(inn_data["is_dismissed"], bool)
        
    
   
   
- Test the search endpoint

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
    
     
   
   
 

### Part 2 — Database Validation
Connect directly to PostgreSQL and write tests that:
- Verify data integrity after API operations (e.g., dismiss a finding via API → query DB → verify `is_dismissed` is TRUE)

import pytest
import requests
import psycopg2
URL = "http://localhost:8000"
def test_DataIntergrity(db_cursor):
    response = requests.get(f"{URL}/findings/", params={"page": 1,"per_page": 1})
    assert response.status_code == 200
    is_id = response.json()["items"][0]["id"]
    response_del = requests.delete(f"{URL}/findings/{is_id}")
    assert response_del.status_code == 200
    db_cursor.execute("select is_dismissed FROM findings WHERE id=%s", (is_id,))
    result = db_cursor.fetchone()
    assert result[0] is True 
    print("is_dismissed is successful")

- Check that database constraints enforce data quality (e.g., CVSS score ranges, required fields)

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


        
 
    

     


- Validate consistency between findings, vulnerabilities, and assets tables
import pytest
import requests
import psycopg2
def test_findings_asset_consistency(db_cursor):
    db_cursor.execute("SELECT f.id, f.asset_id FROM findings f LEFT JOIN assets a ON f.asset_id = a.id WHERE a.id IS NULL")
    orphans = db_cursor.fetchall()

    if len(orphans) == 0:
        print("All findings have a valid asset")
    else:
        for row in orphans:
            print("Finding id", row[0], "points to missing asset_id", row[1])

    assert len(orphans) == 0, f"Found {len(orphans)} findings with no matching asset: {orphans}"


def test_findings_vulnerability_consistency(db_cursor):
    db_cursor.execute("""
        SELECT f.id, f.vulnerability_id
        FROM findings f
        LEFT JOIN vulnerabilities v ON f.vulnerability_id = v.id
        WHERE v.id IS NULL
    """)
    orphans = db_cursor.fetchall()

    if len(orphans) == 0:
        print("All findings have a valid vulnerability")
    else:
        for row in orphans:
            print("Finding id", row[0], "points to missing vulnerability_id", row[1])

    assert len(orphans) == 0, f"Found {len(orphans)} findings with no matching vulnerability: {orphans}"

### Part 3 — Integration Testing
Test cross-service flows:
- Run a scan via Scanner Service → verify findings created in Dashboard API
- Update finding status → verify DB state matches
- Test what happens with concurrent scan imports (optional but valuable)

### Part 4 — UI Smoke Test with Playwright
Write 1-2 Playwright tests:
- Navigate to `http://localhost:8000/`, verify the dashboard loads with findings
- Change a finding's status through the UI dropdown and verify the change is reflected

### Part 5 — Bug Report
Document any bugs you found during testing. For each bug:
- **Title** — short description
- **Severity** — Critical / High / Medium / Low
- **Steps to reproduce**
- **Expected vs actual behavior**

---

## Getting Started

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run your tests
pytest
```

Place all test files in the `tests/` directory. You're free to create any folder structure, conftest files, or helper modules you need.

---

## Tips
- The application **has bugs** — finding and documenting them is part of the assessment
- Code quality matters: clean structure, good naming, proper assertions
- Don't spend all your time on one section — coverage across all parts is important
- You can use the interactive API docs at `http://localhost:8000/docs` and `http://localhost:8001/docs`
- The seed data includes real-world CVE references — familiarize yourself with the data before writing tests

Good luck!
