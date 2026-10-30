from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.adapters.api import router
from src.domain import InvalidReviewError


def create_app() -> FastAPI:
    app = FastAPI(title="Doctor Reviews", version="0.1.0")
    app.include_router(router)

    @app.exception_handler(InvalidReviewError)
    async def invalid_review_handler(
        _request: Request,
        exc: InvalidReviewError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.get("/healthcheck")
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8001, reload=True)