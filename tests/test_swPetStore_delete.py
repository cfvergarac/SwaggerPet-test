import pytest
import httpx
from test_swPetStore_fixtures import *


@pytest.mark.asyncio
@pytest.mark.delete
async def test_delete_pet(default_client: httpx.AsyncClient, mock_post_pet, fake_jwt_token):
    """
    Test the deletion of a pet from the store.
    
    This test performs the following steps:
    1. Posts a new pet to the store.
    2. Deletes the posted pet using its ID.
    3. Verifies that the deletion was successful.
    4. Confirms that the pet no longer exists in the store.
    
    Args:
        default_client (httpx.AsyncClient): The HTTP client used to make requests to the API.
        mock_post_pet (dict): The mock data for the pet to be posted.
        fake_jwt_token (str): The fake JWT token for authorization.
    
    Raises:
        pytest.fail: If the response is not in JSON format.
        AssertionError: If any of the assertions fail.
    """

    response = await default_client.post("/pet/", json=mock_post_pet)
    assert response.status_code == 200

    headers = {"Authorization": f"Bearer '{fake_jwt_token}'"}
    pet_id = mock_post_pet["id"]
    response = await default_client.delete(f"/pet/{pet_id}", headers=headers )
    assert response.status_code == 200
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not in JSON format")
    assert data.message == pet_id
    response = await default_client.get(f"/pet/{pet_id}")
    assert response.status_code == 404,"The pet was not deleted"



@pytest.mark.parametrize("pet_id", [
    (99999),
    ("number"),
    (-1),
    (None)
])
@pytest.mark.asyncio
@pytest.mark.delete
async def test_delete_pet_invalid_id(default_client: httpx.AsyncClient, pet_id, fake_jwt_token):
    """
    Test the deletion of a pet with invalid IDs using DDT (Data-Driven Tests).

    This test uses the pytest.mark.parametrize decorator to run the test with multiple invalid pet IDs.
    It verifies that the API returns a 400 status code for each invalid ID.

    Args:
        default_client (httpx.AsyncClient): The HTTP client used to send requests to the API.
        pet_id (int or str or None): The ID of the pet to be deleted. This is parameterized to test various invalid IDs.
        fake_jwt_token (str): A fake JWT token used for authorization.

    Assertions:
        Asserts that the response status code is 400 for invalid pet IDs.
    """
    headers = {"Authorization": f"Bearer '{fake_jwt_token}'"}
    response = await default_client.delete(f"/pet/{pet_id}", headers=headers )
    assert response.status_code == 400, "the response code must be 400 for invalid ids"

@pytest.mark.parametrize("pet_id", [
    (0),
    (-1)
])
@pytest.mark.asyncio
@pytest.mark.delete
async def test_delete_pet_not_found(default_client: httpx.AsyncClient, pet_id, fake_jwt_token):
    """
    Test the deletion of a pet that does not exist in the store.

    This test uses DDT  to check the behavior of the delete endpoint
    when attempting to delete pets with invalid IDs. The test is asynchronous and uses the 
    httpx.AsyncClient for making HTTP requests.

    Args:
        default_client (httpx.AsyncClient): The HTTP client used to send requests to the API.
        pet_id (int): The ID of the pet to be deleted. This is parameterized to test multiple invalid IDs.
        fake_jwt_token (str): A fake JWT token used for authorization in the request headers.

    Assertions:
        Asserts that the response status code is 404, indicating that the pet was not found.
    """
    headers = {"Authorization": f"Bearer '{fake_jwt_token}'"}
    response = await default_client.delete(f"/pet/{pet_id}", headers=headers )
    assert response.status_code == 404, "the response code must be 404 for pet not found"
