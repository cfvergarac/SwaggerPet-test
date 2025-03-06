import pytest
import httpx
from test_swPetStore_fixtures import *
from petModel import PetResponse

@pytest.mark.asyncio
@pytest.mark.post
async def test_post_pet(default_client: httpx.AsyncClient, mock_post_pet):
    """
    Test the POST /pet/ endpoint to create a new pet.

    Args:
        default_client (httpx.AsyncClient): The HTTP client to use for the request.
        mock_post_pet (dict): The mock data for the pet to be posted.

    Raises:
        pytest.fail: If the response is not in JSON format.
        pytest.fail: If the response does not have the pet model.
        pytest.fail: If any of the different fields do not match the expected values.
    """
    response = await default_client.post("/pet/", json=mock_post_pet)
    assert response.status_code == 200

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not in JSON format")

    pet_data = PetResponse(**data)
    assert pet_data.id == mock_post_pet["id"], "pet id does not match"
    assert pet_data.name == mock_post_pet["name"], "pet name does not match"
    assert pet_data.status == mock_post_pet["status"], "pet status does not match"
    assert pet_data.category.id == mock_post_pet["category"]["id"], "category id does not match"
    assert pet_data.category.name == mock_post_pet["category"]["name"], "category name does not match"
    assert pet_data.photoUrls == mock_post_pet["photoUrls"], "photoUrls do not match"
    assert pet_data.tags[0].id == mock_post_pet["tags"][0]["id"], "tag id does not match"
    assert pet_data.tags[0].name == mock_post_pet["tags"][0]["name"], "tag name does not match"

@pytest.mark.asyncio
@pytest.mark.post
async def test_post_pet_no_name(default_client: httpx.AsyncClient, mock_post_pet_no_name):
    """
    Test the POST /pet/ endpoint with a payload that lacks a name.

    Args:
        default_client (httpx.AsyncClient): The HTTP client used to make requests to the API.
        mock_post_pet_no_name (dict): The mock payload for the POST request, which does not include a name.

    Assertions:
        Asserts that the response status code is not 200, indicating that an insertion without a name should not be allowed.
    """
    response = await default_client.post("/pet/", json=mock_post_pet_no_name)
    assert response.status_code != 200, "an insertion without a name should not be allowed"

@pytest.mark.asyncio
@pytest.mark.post
async def test_post_pet_invalid_status(default_client: httpx.AsyncClient, mock_post_pet_invalid_status):
    """
    Test the POST /pet/ endpoint with an invalid status.

    Args:
        default_client (httpx.AsyncClient): The HTTP client used to make the request.
        mock_post_pet_invalid_status (dict): The mock data for the pet with an invalid status.

    Assertions:
        Asserts that the response status code is 405, indicating that an insertion with an invalid status should not be allowed.
    """
    response = await default_client.post("/pet/", json=mock_post_pet_invalid_status)
    assert response.status_code == 405, "an insertion with an invalid status should not be allowed"

@pytest.mark.asyncio
@pytest.mark.post
async def test_post_pet_duplicate_id(default_client: httpx.AsyncClient, mock_post_pet):
    """
    Test the POST /pet/ endpoint for handling duplicate pet IDs.

    Args:
        default_client (httpx.AsyncClient): The HTTP client used to make requests to the API.
        mock_post_pet (dict): The mock data representing a pet to be posted.

    Assertions:
        Asserts that the status code of the second POST request is not 200, indicating that the insertion of a duplicate ID is not allowed.
    """
    response = await default_client.post("/pet/", json=mock_post_pet)
    response = await default_client.post("/pet/", json=mock_post_pet)
    assert response.status_code != 200, "an insertion of a duplicate id should not be allowed"

@pytest.mark.asyncio
@pytest.mark.post
async def test_post_pet_id_invalid_dataType(default_client: httpx.AsyncClient, mock_post_pet_string_id):
    """
    Test posting a pet with an invalid data type for the pet ID.

    Args:
        default_client (httpx.AsyncClient): The HTTP client used to make the request.
        mock_post_pet_string_id (dict): The mock data containing a string ID for the pet.

    Assertions:
        Asserts that the response status code is 405, indicating that the insertion of a string ID is not allowed.
    """
    response = await default_client.post("/pet/", json=mock_post_pet_string_id)
    assert response.status_code == 405, "an insertion of a string id should not be allowed"

@pytest.mark.asyncio
@pytest.mark.post
async def test_post_pet_name_invalid_dataType(default_client: httpx.AsyncClient, mock_post_pet_name_int):
    """
    Test the POST /pet/ endpoint with invalid data type for pet name.

    Args:
        default_client (httpx.AsyncClient): The HTTP client used to make the request.
        mock_post_pet_name_int (dict): The mock payload containing an integer as the pet name.

    Assertions:
        Asserts that the response status code is 405, indicating that the insertion of an integer name is not allowed.
    """
    response = await default_client.post("/pet/", json=mock_post_pet_name_int)
    assert response.status_code == 405, "an insertion of an integer name should not be allowed"
