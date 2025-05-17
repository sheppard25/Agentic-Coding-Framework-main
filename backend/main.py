from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World - GRBL Web Controller Backend"}


# To run this app:
# 1. Ensure your virtual environment is activated.
# 2. Navigate to the 'backend' directory in your terminal.
# 3. Run the command: uvicorn main:app --reload
# 4. Open your browser and go to http://127.0.0.1:8000
