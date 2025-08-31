import os
import sys

from fastapi.testclient import TestClient

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


from main import app  # noqa: E402

client = TestClient(app)


def test_create_dish():
    response = client.post(
        "/books/",
        json={
            "name": "Test Dish",
            "ingredients": ["ingredient1", "ingredient2"],
            "detailed_description": "Test description",
            "cook_time": 25,
            "views": 0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Dish"
    assert "id" in data


def test_get_recipes():
    response = client.get("/recipes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_recipe_by_id():
    create_response = client.post(
        "/books/",
        json={
            "name": "Another Dish",
            "ingredients": ["ingredientA"],
            "detailed_description": "Another description",
            "cook_time": 15,
            "views": 0,
        },
    )
    dish_id = create_response.json()["id"]
    response = client.get(f"/recipes/{dish_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == dish_id
    assert data["views"] >= 1  # Проверяем инкремент просмотров
