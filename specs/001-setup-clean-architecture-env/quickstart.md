# Quickstart: FastAPI Clean Architecture Environment Setup

This guide provides the steps to set up and run the project locally.

## Prerequisites

-   Python 3.9+
-   `uv` installed (`pip install uv`)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create the virtual environment:**
    ```bash
    uv venv
    ```

3.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

4.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

## Running the Application

1.  **Start the server:**
    ```bash
    uvicorn src.app.main:app --reload
    ```
    The application will be running at `http://127.0.0.1:8000`.

2.  **Verify the application:**
    Open your browser to `http://127.0.0.1:8000` or use `curl`:
    ```bash
    curl http://127.0.0.1:8000
    ```
    You should see the following response:
    ```json
    {"message":"Hello World"}
    ```
