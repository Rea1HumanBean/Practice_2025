import asyncio
import multiprocessing
from gRPC.grpc_server import run_grpc_server
from src import http_server
import uvicorn


def run_http():
    uvicorn.run(http_server, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    http_process = multiprocessing.Process(target=run_http)
    try:
        http_process.start()
        asyncio.run(run_grpc_server())
    except KeyboardInterrupt:
        http_process.terminate()
        http_process.join()
