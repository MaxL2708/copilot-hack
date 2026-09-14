# Security Fixes

## Fixed Issues

### 1. ✅ CORS Policy Restricted (Critical)
- **Before**: `Access-Control-Allow-Origin: *` allowed any origin
- **After**: Only whitelisted origins allowed (configurable via `ALLOWED_ORIGINS` env var)
- **Impact**: Prevents unauthorized cross-site requests

### 2. ✅ Flask Debug Mode Hardening (High)
- **Before**: `debug=True` always enabled (exposes internal state, enables remote code execution risk)
- **After**: `debug=True` only when `FLASK_DEBUG=true` environment variable is set
- **Impact**: Prevents debug mode in production; safer by default

### 3. ✅ Input Validation Added (High)
- **Before**: No validation on `day_of_week` and `airport_id` parameters; server crashes on invalid input
- **After**: Validates ranges (day_of_week: 1-7, airport_id > 0) and returns 400 errors
- **Impact**: Prevents invalid inputs from crashing the server

### 4. ✅ Error Handling Improved (Medium)
- **Before**: Unhandled exceptions could leak stack traces
- **After**: Try-except block catches errors and returns sanitized JSON responses
- **Impact**: Reduces information disclosure

### 5. ✅ Resource Management (Low)
- **Before**: File handle not explicitly closed in `pickle.load()`
- **After**: Using `with` statement for proper file handling
- **Impact**: Prevents file descriptor leaks

### 6. ✅ Default Credentials Documented (Medium)
- **Before**: Hardcoded `postgres:postgres` with no warning
- **After**: Added comment warning about dev-only use
- **Impact**: Developers aware of insecure defaults

## Remaining Recommendations

- [ ] Use `joblib.load()` instead of `pickle.load()` for ML models (safer)
- [ ] Implement rate limiting on `/predict` endpoint
- [ ] Add request logging and monitoring
- [ ] Use environment-specific configuration (dev/prod)
- [ ] Add security headers (X-Content-Type-Options, X-Frame-Options, etc.)
