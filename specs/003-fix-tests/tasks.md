# Tasks

- [ ] Fix Pydantic Model in `item.py` <!-- id: 0 -->
    - Change `Config` to `ConfigDict`
- [ ] Fix Repository Usage in `in_memory_item_repository.py` <!-- id: 1 -->
    - Change `.dict()` to `.model_dump()`
- [ ] Fix Test Assertion in `test_main.py` <!-- id: 2 -->
    - Update expected JSON
- [ ] Verify fix <!-- id: 3 -->
    - Run `uv run pytest`
