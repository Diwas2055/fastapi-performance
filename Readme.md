# Guide to increase the performance of your FastAPI application

> List of tips to increase the performance of your FastAPI application

1. Use `uvloop` (+10%) , uvloop is a fast,drop-in replacement of the built-in asyncio event loop.
2. Use `httptools` (+10%) , "fast parsing" Python blinding for nodejs HTTP parser ,you just need to install it and it will be used automatically by `uvicorn` .
3. Use bigger thread pool size (+5%) , by default `uvicorn` uses 4 threads , you can increase it by passing `--workers` flag to `uvicorn` command.
4. Use simple async applications (+15%) , no overhead of threads and processes.
5. Remove duplicate validation (+25%), have only FastAPI do this validation.
6. Use `ORJSON` (+5%), if not using the lastest Pydantic version already.
