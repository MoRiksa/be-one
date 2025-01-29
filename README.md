# BE-ONE

This is a FastAPI project powered by [Uvicorn](https://www.uvicorn.org/) for high-performance ASGI applications.

## Getting Started

First, set up your virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

Then, run the development server:

```bash
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to see the API documentation.

You can start editing the project by modifying `main.py`. The server will auto-reload as you edit the file if `--reload` is used.

## Learn More

To learn more about FastAPI and Uvicorn, take a look at the following resources:

- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Learn about FastAPI features and API.
- [Uvicorn Documentation](https://www.uvicorn.org/) - High-performance ASGI server.

You can check out [FastAPI's GitHub repository](https://github.com/tiangolo/fastapi) - your feedback and contributions are welcome!

## Deploy on Production

For production deployment, consider using:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use a process manager like **Gunicorn** with **Uvicorn workers**:

```bash
gunicorn -k uvicorn.workers.UvicornWorker -w 4 main:app
```

Check out the [FastAPI deployment documentation](https://fastapi.tiangolo.com/deployment/) for more details.
