# Bug Report — QA Technical Assessment
## Part 5 — Bug Report

---

### Bug 1 — Database Connection Failure on Service Startup

**Title:** Scanner Service fails to connect to PostgreSQL on startup — hostname "postgres" cannot be resolved

**Severity:** Critical

**Steps to Reproduce:**
1. Follow README setup instructions
2. Run `docker compose up`
3. Observe Scanner Service logs at startup

**Expected:**
Both services start successfully and connect to PostgreSQL without errors.

**Actual:**
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) 
could not translate host name "postgres" to address: 
Name or service not known
```
Service fails to resolve the hostname `postgres` — database connection is never established.

**Impact:** Critical — the Scanner Service cannot start properly, meaning all scan operations and any endpoint relying on the database are unavailable until the connection issue is resolved. Blocks Part 3 integration testing entirely.

---

### Bug 2 — Trailing Slash and Wrong Path Cause 404 on Valid Endpoints

**Title:** GET `/assets.` and GET `/findings` return 404 Not Found

**Severity:** High

**Steps to Reproduce:**
1. Start the application via `docker compose up`
2. Send `GET http://localhost:8001/assets.` in browser or Postman
3. Send `GET http://localhost:8000/findings` in browser or Postman
4. Observe response codes

**Expected:**
```
GET /assets    → 200 OK with paginated asset list
GET /findings  → 200 OK with paginated findings list
```

**Actual:**
```
GET /assets.   → 404 Not Found
GET /findings  → 404 Not Found
GET /          → 404 Not Found
```

**Impact:** High — core API endpoints return 404, making the dashboard and scanner service inaccessible via direct URL navigation. The root `/` endpoint also returns 404, meaning the Dashboard UI does not load.

---

### Bug 3 — Incorrect Database Credentials in Project Setup

**Title:** Auto-generated conftest.py contains incorrect database credentials — missing underscores

**Severity:** Medium

**Steps to Reproduce:**
1. Follow the README setup instructions
2. Run `pytest tests/db_validation.py`
3. Observe connection failure in terminal

**Expected:**
conftest.py connects successfully using credentials from README:
- dbname=qa_test, user=qa_user, password=qa_password

**Actual:**
Connection fails with:
```
psycopg2.OperationalError: FATAL: password authentication failed for user "qauser"
```
Generated file uses qatest / qauser / qapassword — underscores missing throughout.

**Impact:** Medium — any tester following the setup guide cannot run database validation tests without manually correcting credentials. Blocks Part 2 testing entirely.

---

### Bug 4 — DELETE /findings/{id} Returns 204 Instead of 200

**Title:** DELETE /findings/{id} returns 204 No Content instead of documented 200 OK

**Severity:** Low

**Steps to Reproduce:**
1. Start the application via `docker compose up`
2. Send `DELETE http://localhost:8000/findings/1`
3. Observe response status code

**Expected:**
```
200 OK with confirmation body e.g. { "message": "finding dismissed" }
```

**Actual:**
```
204 No Content with empty response body
```

**Impact:** Low — any client code or test asserting 200 on DELETE will incorrectly fail. The behaviour itself is technically valid HTTP but contradicts the implied API contract in the README documentation.

---

*Report prepared by: Vithyali Yoganathan*
*Date: 21 April 2026*
*Assessment: QA Automation Engineer — Technical Assessment*
