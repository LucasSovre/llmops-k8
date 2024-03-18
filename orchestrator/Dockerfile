FROM python:3.10-slim-bullseye 
#LTS version of python

LABEL org.opencontainers.image.source="https://github.com/LucasSovre/llmops-k8"

# Set the working directory in the container
WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

COPY ./app/ ./app

# Run the application
EXPOSE 8080

HEALTHCHECK --retries=3 --start-period=5s CMD curl  --fail http://localhost:8080/utils/ || exit 1 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
