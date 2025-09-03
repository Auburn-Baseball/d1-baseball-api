# My FastAPI App

This is a basic FastAPI application structured for easy development and testing.

## Setup Instructions

1. **Install Poetry:**
   Follow the instructions at [Poetry's official website](https://python-poetry.org/docs/#installation) to install Poetry.

2. **Install dependencies:**
   ```
   poetry install
   ```

3. **Run the application:**
   ```
   poetry run uvicorn d1_baseball_api.main:app --reload
   ```

## Usage

Once the application is running, you can access the API at `http://127.0.0.1:8000`. You can also access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Testing

To run the tests, use the following command:
```
poetry run pytest
```

## License

This project is licensed under the MIT License.