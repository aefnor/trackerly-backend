# Use the official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./backend ./backend

# Expose the application port
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn (uvicorn is already installed in the venv)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
