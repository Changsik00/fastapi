# Implementation Plan

## Proposed Changes

### Tests
#### [MODIFY] [tests/contract/test_main.py](file:///Users/ck/Project/Changsik/fastapi/tests/contract/test_main.py)
- Update expected JSON in `test_read_main`.

### Domain Models
#### [MODIFY] [src/domain/models/item.py](file:///Users/ck/Project/Changsik/fastapi/src/domain/models/item.py)
- Replace `class Config: orm_mode = True` with `model_config = ConfigDict(from_attributes=True)`.

### Infrastructure
#### [MODIFY] [src/infrastructure/repositories/in_memory_item_repository.py](file:///Users/ck/Project/Changsik/fastapi/src/infrastructure/repositories/in_memory_item_repository.py)
- Replace `item.dict()` with `item.model_dump()`.

## Verification Plan
1. Run `uv run pytest` and verify:
    - 0 failures.
    - No Pydantic warnings in stdout/stderr.
