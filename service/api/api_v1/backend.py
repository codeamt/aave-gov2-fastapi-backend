import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from ..routes.propoals import aave_proposals_router


def get_application() -> FastAPI:
    app = FastAPI(root_path="/api/v1")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["localhost"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"])

    @app.get("/", summary="", tags=["Index/Root"])
    def main():
        return {"data": "index_route"}

    @app.get("/ping", summary="", tags=["Index/Root"])
    def healthcheck():
        return {"data": "pong"}

    app.include_router(aave_proposals_router)

    def documentation_configs():
        if app.openapi_schema:
            return app.openapi_schema
        meta = get_openapi(
            title="AAVE Governance V2 Dashboard",
            version="1.0.0",
            description="Backend Server for AAVE Governance V2 Protocol (Proposals)",
            routes=app.routes,
        )
        app.openapi_schema = meta
        return app.openapi_schema

    app.openapi = documentation_configs
    return app


server = get_application()


@server.on_event("startup")
async def startup():
    pass


@server.on_event("shutdown")
async def shutdown():
    pass

if __name__ == "__main__":
    uvicorn.run("backend:server", host="0.0.0.0", port=8080)