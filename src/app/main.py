from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Clean Architecture",
    description="An example of a FastAPI application following clean architecture principles.",
    version="0.1.0",
)

# No router included by default. Routers will be included explicitly where needed (e.g., in tests).

@app.get("/")
def read_root():
    return {"message": "Welcome to the Clean Architecture example!"}
