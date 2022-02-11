import uvicorn
from service.api.api_v1.backend import server


if __name__ == "__main__":
    uvicorn.run(server, host="0.0.0.0", port=8080)
