# Use the official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the requirements file into the container
COPY requirements.txt .

# Copy pyproject.toml and poetry.lock files into the container
COPY pyproject.toml .

# Copy the uv.lock file into the container
COPY uv.lock .

# Create virtual environment and install dependencies in a single RUN command
# to keep the layer size smaller
RUN uv venv \
    && uv pip install --upgrade pip \
    && uv pip install -r requirements.txt

# Copy the application code into the container
COPY ./backend ./backend

# Expose the application port
EXPOSE 8000

# CD into app/backend
WORKDIR /app/backend

# Install uvicorn globally so it's available in PATH
RUN pip install uvicorn

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
