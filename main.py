import anyio
import httpx
import uvicorn
import uvloop
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator


# Define a Pydantic model with validation
class Item(BaseModel):
    name: str
    description: str

    @validator("name")
    def validate_name_length(cls, v):
        if len(v) < 3:
            raise ValueError("Name must be at least 3 characters")
        return v


# Anyio is a library that provides an asynchronous compatibility layer for the standard library.
async def startup():
    # The line `limiter = anyio.to_thread.current_default_thread_limiter()` is creating a limiter
    # object that controls the number of threads that can be used concurrently. It is using the
    # `current_default_thread_limiter()` function from the `anyio.to_thread` module to get the default
    # limiter for the current thread.
    limiter = anyio.to_thread.current_default_thread_limiter()
    # The line `limiter.total_tokens = 1000` is setting the total number of tokens available in the
    # limiter object to 1000.
    limiter.total_tokens = 1000


# Some asynchronous task that simulates making an API request
async def make_api_request(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


app = FastAPI(on_startup=[startup])


@app.get("/")
async def root():
    return JSONResponse({"message": "Hello World"})


# FastAPI route to trigger the asynchronous task
@app.get("/api-request")
async def api_request_handler():
    url = "https://jsonplaceholder.typicode.com/todos/1"
    result = await make_api_request(url)
    return result


# Custom dependency for validating the item data
def validate_item_data(item: Item = Depends()):
    return item


# Route function using the custom dependency for validation
@app.post("/items/")
async def create_item(item_data: Item = Depends(validate_item_data)):
    # Process the validated item data and create the item
    return {"message": "Item created successfully"}


if __name__ == "__main__":
    # `uvloop.install()` is a function that installs the `uvloop` event loop policy as the default
    # event loop policy for asyncio. The `uvloop` library is a fast, drop-in replacement for the
    # standard asyncio event loop. By installing `uvloop`, the code is using a more efficient event
    # loop implementation, which can result in better performance for the application.
    uvloop.install()  # Install the uvloop event loop policy for better performance
    uvicorn.run("main:app", host="0.0.0.0", port=9000, http="httptools", reload=True)
