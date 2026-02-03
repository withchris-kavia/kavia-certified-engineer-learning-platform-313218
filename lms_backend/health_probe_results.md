# Backend health probe results

Target base URL: `http://127.0.0.1:3001`  
Timestamp (UTC): 2026-02-03

## Summary
Backend is reachable. `/health` and `/` returned 200 OK. `/api/health` is not registered (404).

## Attempts (in order)

1. `GET /health`  
   - HTTP 200
   - Body: `{"status":"ok"}`

2. `GET /api/health`  
   - HTTP 404
   - Body: `{"detail":"Not Found"}`

3. `GET /`  
   - HTTP 200
   - Body: `{"service":"lms_backend","status":"ok"}`
