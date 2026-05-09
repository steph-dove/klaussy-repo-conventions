---
paths:
  - "scripts/**/*.py"
---

# Rules for `scripts/**/*.py`

## Conventions

- **Context manager usage**: Uses context managers for resource management. 25 with statements (17 sync, 8 async). Types: file_io (2).
- **Structured configuration with Pydantic Settings**: Uses Pydantic BaseSettings for configuration management
