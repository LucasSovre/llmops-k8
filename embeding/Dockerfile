FROM python:3.10-bullseye 
#LTS version of python

LABEL org.opencontainers.image.source="https://github.com/LucasSovre/llmops-k8"

# Set the working directory in the container
WORKDIR /code

#download the model first to optimize docker cache
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && apt-get install git-lfs -y
COPY downloadmodel.sh .
RUN bash downloadmodel.sh

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt --prefer-binary 

COPY embedingserver.py .

CMD ["python", "embedingserver.py"]
