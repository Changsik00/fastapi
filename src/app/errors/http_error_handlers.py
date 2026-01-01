from fastapi import Request
from fastapi.responses import JSONResponse

async def http_404_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "code": "NOT_FOUND",
            "message": "The requested resource was not found",
            "path": request.url.path
        },
    )
