import pytest
import httpx
from test_swPetStore_utils import default_client
from test_swPetStore_utils import mock_get_pet
from petModel import PetResponse


@pytest.mark.asyncio
async def test_get_pet_by_id_success(default_client: httpx.AsyncClient, mock_get_pet):
    """
    Test the successful retrieval of a pet by its ID.

    Args:
        default_client (httpx.AsyncClient): The HTTP client used to make requests to the API.
        mock_get_pet (dict): Mocked data representing the expected response from the API.

    Raises:
        pytest.fail: If the response is not in JSON format.

    Asserts:
        The response status code matches the expected status (404).
        The response JSON contains the correct error code.
        The response JSON contains the correct error type.
        The response JSON contains the correct error message.
    
    """
    pet_id = mock_get_pet["id"]
    response = await default_client.get(f"/pet/{pet_id}")
    assert response.status_code == 200
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not in JSON format")
    pet_data = PetResponse(**data)
    assert pet_data.id == mock_get_pet["id"], "pet id does not match"
    assert pet_data.category.id == mock_get_pet["category"]["id"], "category id does not match"
    assert isinstance(pet_data.photoUrls, list) , "photoUrls must be a list"
    assert isinstance(pet_data.tags, list), "tags do not match"
    


"""
Fixture to define the data for test_get_pet_by_id_pet_not_found function in DDT style
"""
@pytest.mark.parametrize("pet_id, expected_status", [
    (0, 404),
    (-1, 404),
    (999999999, 404)
])

@pytest.mark.asyncio
async def test_get_pet_by_id_pet_not_found(pet_id, expected_status, default_client: httpx.AsyncClient):
    """
    Negative test cases for getting a pet by non valid ID get a 404 error.

    Args:
        pet_id (int): The ID of the pet to retrieve.
        expected_status (int): The expected HTTP status code.
        default_client (httpx.AsyncClient): The HTTP client to use for making the request.

    Raises:
        pytest.fail: If the response is not in JSON format.
        pytest.fail: If the status code is not 404
        pytest.fail: If the response does not have the right data

    Asserts:
        The response status code matches the expected status (404).
        The response JSON contains the correct error code.
        The response JSON contains the correct error type.
        The response JSON contains the correct error message.
    """
    response = await default_client.get(f"/pet/{pet_id}")
    assert response.status_code == expected_status
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not in JSON format")
    assert data["code"] == 1, f"Expected code error is 1, obtained: {data['code']}"
    assert data["type"] == "error", f"Expected type error is error, obtained: {data['type']}"
    assert data["message"] == "Pet not found", f"Expected code message is Pet not found, obtained: {data['message']}"


"""
Fixture to define the data for test_get_pet_by_id_pet_invalid_input function in DDT style
"""
@pytest.mark.parametrize("pet_id, expected_status", [
    (0.5, 404),
    ("number", 404),
    ( None, 404)
])
@pytest.mark.asyncio
async def test_get_pet_by_id_pet_invalid_input(pet_id, expected_status, default_client: httpx.AsyncClient):
    """
    Negative test cases for getting a pet by non valid ID, get a 404 error.

    Args:
        pet_id (int): The ID of the pet to retrieve.
        expected_status (int): The expected HTTP status code.
        default_client (httpx.AsyncClient): The HTTP client to use for making the request.

    Raises:
        pytest.fail: If the status code is not 404
    """
    response = await default_client.get(f"/pet/{pet_id}")
    assert response.status_code == expected_status


  


