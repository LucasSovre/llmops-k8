FROM python:3.10-bullseye 
#LTS version of python

# Set the working directory in the container
WORKDIR /code

#download the model first to optimize docker cache
COPY downloadmodel.sh .
RUN bash downloadmodel.sh

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt --prefer-binary 

COPY llmserver.py .

CMD ["python", "llmserver.py"]
