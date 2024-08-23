import requests
import pytest
from jsonschema import validate, ValidationError


BASE_URL = "https://petstore.swagger.io/v2/pet"

# Данные для создания питомца
pet_data = {
    "id": 123456,
    "name": "Killer",
    "category": {"id": 1, "name": "Dog"},
    "photoUrls": ["https://example.com"],
    "tags": [{"id": 1, "name": "friendly"}],
    "status": "available"
}

# JSON-схема для валидации ответа
pet_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "category": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"}
            },
            "required": ["id", "name"]
        },
        "photoUrls": {
            "type": "array",
            "items": {"type": "string"}
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                },
                "required": ["id", "name"]
            }
        },
        "status": {"type": "string"}
    },
    "required": ["id", "name", "category", "photoUrls", "tags", "status"]
}


# POST: Add a new pet
def test_create_pet():
    response = requests.post(BASE_URL, json=pet_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == pet_data['id']
    assert response_data['name'] == pet_data['name']

    try:
        validate(instance=response_data, schema=pet_schema)
    except ValidationError as e:
        pytest.fail(f"Response did not match schema: {e}")

    assert response_data['id'] == pet_data['id']
    assert response_data['name'] == pet_data['name']

# GET: Find pet by id
def test_get_pet():
    response = requests.get(f"{BASE_URL}/{pet_data['id']}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == pet_data['id']
    assert response_data['name'] == pet_data['name']

    try:
        validate(instance=response_data, schema=pet_schema)
    except ValidationError as e:
        pytest.fail(f"Response did not match schema: {e}")

    assert response_data['id'] == pet_data['id']
    assert response_data['name'] == pet_data['name']

# PUT: Update pet
def test_update_pet():
    updated_data = pet_data.copy()
    updated_data['name'] = "Fluffy"
    response = requests.put(BASE_URL, json=updated_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['name'] == "Fluffy"

    try:
        validate(instance=response_data, schema=pet_schema)
    except ValidationError as e:
        pytest.fail(f"Response did not match schema: {e}")

    assert response_data['name'] == "Fluffy"

# DELETE: Delete pet
def test_delete_pet():
    response = requests.delete(f"{BASE_URL}/{pet_data['id']}")
    assert response.status_code == 200
get_response = requests.get(f"{BASE_URL}/{pet_data['id']}")
assert get_response.status_code == 404

#@pytest.mark.parametrize("pet_id", [123456, 789012, 345678])
#def test_delete_pet(pet_id):
   # response = requests.delete(f"{BASE_URL}/{pet_id}")
    #assert response.status_code == 200

