import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def wait_for_server(url, max_retries=10, retry_delay=1):
    print(f"Waiting for server at {url} to be ready...")
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=retry_delay)
            if response.status_code == 200:
                print("Server is ready!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        print(f"Server not ready, retrying in {retry_delay}s...")
        time.sleep(retry_delay)
    print("Server did not become ready within the timeout.")
    return False

def validate():
    print("\n--- Validating Quickstart Commands ---")

    # Ensure server is running and responsive
    if not wait_for_server(BASE_URL):
        print("Validation aborted: Server is not reachable.")
        return

    item_id = None

    # 1. Create an item
    print("\n1. Creating an item...")
    create_payload = {"name": "My Item", "description": "A cool new item"}
    try:
        response = requests.post(f"{BASE_URL}/items/", json=create_payload)
        response.raise_for_status()
        created_item = response.json()
        item_id = created_item.get("id")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {json.dumps(created_item, indent=2)}")
        assert response.status_code == 201
        assert created_item["name"] == create_payload["name"]
        assert created_item["description"] == create_payload["description"]
        assert item_id is not None
        print("  Assertion Passed: Item created successfully.")
    except requests.exceptions.RequestException as e:
        print(f"  Error creating item: {e}")
        if e.response: print(f"  Response: {e.response.text}")
        return

    # 2. Read all items
    print("\n2. Reading all items...")
    try:
        response = requests.get(f"{BASE_URL}/items/")
        response.raise_for_status()
        all_items = response.json()
        print(f"  Status: {response.status_code}")
        print(f"  Response: {json.dumps(all_items, indent=2)}")
        assert response.status_code == 200
        assert any(item.get("id") == item_id for item in all_items)
        print("  Assertion Passed: All items read successfully.")
    except requests.exceptions.RequestException as e:
        print(f"  Error reading all items: {e}")
        if e.response: print(f"  Response: {e.response.text}")
        return

    # 3. Read a specific item (e.g., item_id=1)
    print(f"\n3. Reading specific item (ID: {item_id})...")
    try:
        response = requests.get(f"{BASE_URL}/items/{item_id}")
        response.raise_for_status()
        specific_item = response.json()
        print(f"  Status: {response.status_code}")
        print(f"  Response: {json.dumps(specific_item, indent=2)}")
        assert response.status_code == 200
        assert specific_item["id"] == item_id
        assert specific_item["name"] == create_payload["name"]
        print("  Assertion Passed: Specific item read successfully.")
    except requests.exceptions.RequestException as e:
        print(f"  Error reading specific item: {e}")
        if e.response: print(f"  Response: {e.response.text}")
        return

    # 4. Update an item (e.g., item_id=1)
    print(f"\n4. Updating item (ID: {item_id})...")
    update_payload = {"name": "My Updated Item", "description": "An even cooler item"}
    try:
        response = requests.put(f"{BASE_URL}/items/{item_id}", json=update_payload)
        response.raise_for_status()
        updated_item = response.json()
        print(f"  Status: {response.status_code}")
        print(f"  Response: {json.dumps(updated_item, indent=2)}")
        assert response.status_code == 200
        assert updated_item["id"] == item_id
        assert updated_item["name"] == update_payload["name"]
        print("  Assertion Passed: Item updated successfully.")
    except requests.exceptions.RequestException as e:
        print(f"  Error updating item: {e}")
        if e.response: print(f"  Response: {e.response.text}")
        return

    # 5. Delete an item (e.g., item_id=1)
    print(f"\n5. Deleting item (ID: {item_id})...")
    try:
        response = requests.delete(f"{BASE_URL}/items/{item_id}")
        response.raise_for_status()
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        assert response.status_code == 200
        assert response.json() == {"message": "Item deleted successfully"}
        print("  Assertion Passed: Item deleted successfully.")

        # Verify deletion
        response = requests.get(f"{BASE_URL}/items/{item_id}")
        assert response.status_code == 404
        print("  Assertion Passed: Item confirmed deleted.")
    except requests.exceptions.RequestException as e:
        print(f"  Error deleting item: {e}")
        if e.response: print(f"  Response: {e.response.text}")
        return

    print("\n--- Quickstart Validation Complete ---")

if __name__ == "__main__":
    validate()
