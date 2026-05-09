---
paths:
  - "tests/**/*.py"
---

# Rules for `tests/**/*.py`

## Conventions

- **HTTP errors raised in service layer**: HTTPException is frequently raised outside the API layer
- **Mocking with unittest.mock / Mock**: Uses unittest.mock / Mock for test mocking. Also uses: pytest monkeypatch fixture, @patch decorator.
- **Test naming: Simple style (test_feature)**: Uses Simple style (test_feature) naming. 2006/2047 (98%) test functions.
