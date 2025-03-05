import pytest
import httpx
import asyncio

BASE_URL = "https://petstore.swagger.io/v2"


"""
Test the GET /pet/{pet_id} endpoint for cases where the pet is not found.
    
This test uses parameterized inputs to check the response for different pet IDs that must not exist.
It verifies that the API returns a 404 status code and the correct error message.
"""
@pytest.mark.parametrize("pet_id, expected_status", [
    (0, 404),
    (-1, 404),
    (999999999, 404)
])

@pytest.mark.asyncio
async def test_get_pet_by_id_pet_not_found(pet_id, expected_status):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/pet/{pet_id}")
    data = response.json()
    assert response.status_code == expected_status
    assert data["code"] == 1, f"Expected code error is 1, obtained: {data['code']}"
    assert data["type"] == "error", f"Expected type error is error, obtained: {data['type']}"
    assert data["message"] == "Pet not found", f"Expected code message is Pet not found, obtained: {data['message']}"


  


