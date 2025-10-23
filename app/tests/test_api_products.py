import pytest
from httpx import AsyncClient, ASGITransport
import pytest_asyncio

from main import application
from app.core.schemas import Product


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=application),
        base_url="http://test",
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_get_products(async_client):
    response = await async_client.get("/api/v1/products/")
    assert response.status_code == 200

    products = response.json()
    assert isinstance(products, list)

    for product in products:
        product_schema = Product(**product)
        assert isinstance(product_schema.id, int)
        assert isinstance(product_schema.name, str)


@pytest.mark.asyncio
async def test_create_and_delete_product(async_client):
    response = await async_client.post(
        "/api/v1/products/",
        json={"name": "test_product"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "test_product"

    created_product_id = response.json()["id"]

    response2 = await async_client.delete(
        f"/api/v1/products/{created_product_id}/",
    )
    assert response2.status_code == 204

    response_check = await async_client.get(
        f"/api/v1/products/{created_product_id}/",
    )
    assert response_check.status_code == 404


@pytest.mark.asyncio
async def test_get_product_by_id(async_client):
    response = await async_client.get(f"/api/v1/products/{3}/")
    assert response.status_code == 200

    product = response.json()
    assert product["id"] == 3
    assert product["name"] == "Апельсин"


@pytest.mark.asyncio
async def test_update_product(async_client):
    response = await async_client.put(
        "/api/v1/products/24/",
        json={"name": "Помидор"},
    )
    assert response.status_code == 200

    updated_product = response.json()
    assert updated_product["id"] == 24
    assert updated_product["name"] == "Помидор"

    response2 = await async_client.put(
        "/api/v1/products/24/",
        json={"name": "Томат"},
    )
    updated_product = response2.json()
    assert updated_product["id"] == 24
    assert updated_product["name"] == "Томат"
