import httpx
import pytest
import jwt
import datetime

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

@pytest.fixture
def fake_jwt_token():
    """Fixture to generate a fake JWT token."""
    payload = {
        "username": "test_user"   
    }
    token = jwt.encode(payload, BASE_URL, algorithm="HS256")
    return token

"""
Fixture to define pet data values for get test validations
"""
@pytest.fixture
async def mock_get_pet():
    return {
    "id": 1,
    "category": {
    "id": 0,
    "name": ""
    },
    "name": "",
    "photoUrls": [],
    "tags": [],
    "status": ""
    }

"""
Fixture to define pet data values for post test validations
"""
@pytest.fixture
async def mock_post_pet():
    return {
    "id": 101,
    "category": {
    "id": 1,
    "name": "cat"
    },
    "name": "boy",
    "photoUrls": [
        "path/to/photo"
    ],
    "tags": [
        {
        "id": 506,
        "name": "good"
        }
    ],
    "status": "sold"
    }

"""
Fixture to define pet data values for post test validations without the mandatory field name
"""
@pytest.fixture
async def mock_post_pet_no_name():
    return {
    "id": 101,
    "category": {
    "id": 1,
    "name": "cat"
    },
    "photoUrls": [
        "path/to/photo"
    ],
    "tags": [
        {
        "id": 506,
        "name": "good"
        }
    ],
    "status": "sold"
    }

"""
Fixture to define pet data values for post test validations with invalid status 
"""
@pytest.fixture
async def mock_post_pet_invalid_status():
    return {
    "id": 101,
    "category": {
    "id": 1,
    "name": "cat"
    },
    "name": "boy",
    "photoUrls": [
        "path/to/photo"
    ],
    "tags": [
        {
        "id": 506,
        "name": "good"
        }
    ],
    "status": "vendido"
    }

"""
Fixture to define pet data values for post test validations with id as a string
"""
@pytest.fixture
async def mock_post_pet_string_id():
    return {
    "id": "101",
    "category": {
    "id": 1,
    "name": "cat"
    },
    "name": "boy",
    "photoUrls": [
        "path/to/photo"
    ],
    "tags": [
        {
        "id": 506,
        "name": "good"
        }
    ],
    "status": "sold"
    }

"""
Fixture to define pet data values for post test validations with name as integer
"""
@pytest.fixture
async def mock_post_pet_name_int():
    return {
    "id": "101",
    "category": {
    "id": 1,
    "name": "cat"
    },
    "name": 13,
    "photoUrls": [
        "path/to/photo"
    ],
    "tags": [
        {
        "id": 506,
        "name": "good"
        }
    ],
    "status": "sold"
    }