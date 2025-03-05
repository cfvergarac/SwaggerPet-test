import httpx
import pytest
import pydantic

BASE_URL = "https://petstore.swagger.io/v2"


"""
Fixture to provide a default HTTP client for testing.

This fixture creates an instance of `httpx.AsyncClient` with the base URL set to `BASE_URL`.
The client instance is yielded for use in tests and is automatically closed after the test completes.

Yields:
    httpx.AsyncClient: An asynchronous HTTP client configured with the base URL.
"""
@pytest.fixture
async def default_client():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        yield client


"""
Fixture to define data values for test_get_pet_by_id_success validations, some values are empty because the response  of API always change
"""
@pytest.fixture
async def mock_get_pet():
    return {
    "id": 1,
    "category": {
    "id": 1,
    "name": ""
    },
    "name": "",
    "photoUrls": [],
    "tags": [],
    "status": ""
    }