import asyncio

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import status

from microservice_api.todo.schemas import CreateTaskSchema, Status, Priority
from microservice_api.todo.server import server


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(server):
        async with httpx.AsyncClient(app=server, base_url="http://app.io") as test_client:
            yield test_client


@pytest.mark.asyncio
async def test_hello_world(test_client: httpx.AsyncClient):
    response = await test_client.get("/todo")

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json == {'tasks': []}


@pytest.mark.asyncio
class TestCreateTodo:
    async def test_valid(self, test_client: httpx.AsyncClient):
        task = CreateTaskSchema(
            status = Status.pending.value,
            priority = Priority.low.value,
            task = "Testing"
        ).model_dump(mode="json")

        # alternatively one could use:
        # task = {
        #     "priority": "low",
        #     "status": "pending",
        #     "task": "string"
        # }


        response = await test_client.post("/todo", json=task)

        assert response.status_code == status.HTTP_201_CREATED
