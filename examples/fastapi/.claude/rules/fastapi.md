---
paths:
  - "fastapi/**/*.py"
---

# Rules for `fastapi/**/*.py`

## Conventions

- **URL-based API versioning**: Uses URL path versioning (e.g., /v1/, /api/v2/)
- **Data class style: Pydantic for API + dataclasses for internal**: Uses Pydantic for API schemas (62) and dataclasses for internal DTOs (6). Good separation.
- **Background jobs with FastAPI BackgroundTasks**: Uses FastAPI BackgroundTasks for background task processing
- **Data classes: Pydantic models**: Uses Pydantic models for structured data. 84/98 structured classes use this pattern.
- **lowercase constant naming**: Uses lowercase naming for module-level values. 87/91 use lowercase.
- **Enum usage: Enum**: Uses Python enums for categorical values. Found 4 enum class(es).
- **Limited exception chaining**: Rarely uses 'raise X from Y'. 7/66 (11%) raises use chaining. Use 'raise X from Y' to preserve context or 'raise X from None' to suppress.
- **Pydantic validation**: Uses Pydantic validation for input validation. 17/28 (61%) validation patterns use this approach.
