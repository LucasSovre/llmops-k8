FROM python:3.10-slim-bullseye 
#LTS version of python

# Set the working directory in the container
WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/ ./app

# Run the application
EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
