# Backend health probe results

Target base URL: `http://127.0.0.1:3001`  
Timestamp (UTC): 2026-02-03

## Summary
No endpoints succeeded (no 2xx). All requests failed with: `curl: (7) Failed to connect ... Couldn't connect to server`.

## Attempts (in order)

1. `GET /health`  
   - Result: network error (connection refused)

2. `GET /api/health`  
   - Result: network error (connection refused)

3. `GET /ready`  
   - Result: network error (connection refused)

4. `GET /live`  
   - Result: network error (connection refused)

5. `GET /`  
   - Result: network error (connection refused)
