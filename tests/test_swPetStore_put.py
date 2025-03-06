import pytest
import httpx
from test_swPetStore_fixtures import *
from petModel import PetResponse


@pytest.mark.asyncio
@pytest.mark.put
async def test_put_pet(default_client: httpx.AsyncClient, mock_post_pet):
    """
    Test the PUT /pet/ endpoint to update a pet's information.

    This test first creates a new pet using the POST /pet/ endpoint, then updates the pet's name using the PUT /pet/ endpoint.
    It verifies that the response status code is 200 and that the pet's information is correctly updated.

    Args:
    default_client (httpx.AsyncClient): The HTTP client used to make requests to the API.
    mock_post_pet (dict): The mock data used to create a new pet.

    Raises:
    pytest.fail: If the response is not in JSON format.

    Asserts:
    response.status_code == 200: The response status code should be 200.
    pet_data.id == mock_post_pet["id"]: The pet ID should match the ID of the created pet.
    pet_data.name == "joey": The updated pet name should be "joey".
    """
    response = await default_client.post("/pet/", json=mock_post_pet)
    data = response.json()
    data["name"] = "joey"
    response = await default_client.put("/pet/", json=data)
    assert response.status_code == 200
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not in JSON format")
    pet_data = PetResponse(**data)
    assert pet_data.id == mock_post_pet["id"], "pet id does not match"
    assert pet_data.name == "joey", "updated pet name does not match"


@pytest.mark.asyncio
@pytest.mark.put
@pytest.mark.parametrize("required_field", [
    ("photoUrls"), ("name"),
])
async def test_put_pet_required_fields(default_client: httpx.AsyncClient, mock_post_pet, required_field):
    """
    Test the PUT /pet/ endpoint for required fields.

    This test uses the ddt (data-driven testing) approach to verify that the PUT /pet/ endpoint
    returns a 405 status code when required fields are missing in the update request.

    Args:
    default_client (httpx.AsyncClient): The HTTP client used to make requests to the API.
    mock_post_pet (dict): A mock pet object used to create a new pet.
    required_field (str): The required field to be removed from the update request.

    Asserts:
    The response status code should be 405 when a required field is missing in the update request.
"""
    response = await default_client.post("/pet/", json=mock_post_pet)
    data = response.json()
    del data[required_field]
    response = await default_client.put("/pet/", json=data)
    assert response.status_code == 405,f"Response status should be 405, {required_field} is missing in update request"

@pytest.mark.parametrize("pet_id", [
    (0), 
    (-1),
    (None),
    ("one")
])
@pytest.mark.asyncio
@pytest.mark.put
async def test_put_pet_invalid_id(default_client: httpx.AsyncClient, mock_post_pet, pet_id):
    """
    Test updating a pet with invalid IDs using PUT method.

    This test uses ddt to test multiple invalid pet IDs. It ensures that the API returns a 400 status code for 
    each invalid ID.

    Args:
        default_client (httpx.AsyncClient): The HTTP client used to make requests to the API.
        mock_post_pet (dict): The mock data for creating a new pet.
        pet_id (int, str, None): The invalid pet ID to test.

    Raises:
        AssertionError: If the response status code is not 400 for an invalid pet ID.
    """
    response = await default_client.post("/pet/", json=mock_post_pet)
    data = response.json()
    data["id"] = pet_id
    response = await default_client.put("/pet/", json=data)
    assert response.status_code == 400, f"Response status should be 400, invalid id {pet_id} in update request"

 
   

