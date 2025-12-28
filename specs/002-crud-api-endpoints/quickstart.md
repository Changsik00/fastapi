# Quickstart: CRUD API Endpoints

This guide explains how to test the new CRUD endpoints for Items.

## Running the Application

1.  Ensure the application is running:
    ```bash
    source .venv/bin/activate
    uvicorn src.app.main:app --reload
    ```

## Testing the Endpoints

You can use `curl` to interact with the API.

**1. Create an item:**
```bash
curl -X POST "http://127.0.0.1:8000/items/" -H "Content-Type: application/json" -d '{"name": "My Item", "description": "A cool new item"}'
```

**2. Read all items:**
```bash
curl http://127.0.0.1:8000/items/
```

**3. Read a specific item (e.g., item_id=1):**
```bash
curl http://127.0.0.1:8000/items/1
```

**4. Update an item (e.g., item_id=1):**
```bash
curl -X PUT "http://127.0.0.1:8000/items/1" -H "Content-Type: application/json" -d '{"name": "My Updated Item", "description": "An even cooler item"}'
```

**5. Delete an item (e.g., item_id=1):**
```bash
curl -X DELETE http://127.0.0.1:8000/items/1
```
