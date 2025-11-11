# Use an official Python base image
FROM python:3.13

# Set working directory
WORKDIR /app

# Copy only dependency files first (for caching)
COPY pyproject.toml uv.lock* ./

# Install uv (if not already included in base image)
RUN pip install uv

# Install dependencies
RUN uv sync --frozen

# Copy the rest of the app
COPY . .

# Expose FastAPI’s default port
EXPOSE 8000

# Run the app using uv and FastAPI’s built-in runner
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
