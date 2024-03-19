if docker info >/dev/null 2>&1; then
    :
else
    echo "Docker is not running or need sudo. Please start Docker and try again."
    exit 1
fi

#start a local docker registry

docker run -d -p 5000:5000 --name registry registry:2

#build the docker images

cd llm && docker build -t llm . && cd ..
cd embeding && docker build -t embbeding . && cd ..
cd orchestrator && docker build -t orchestrator . && cd ..

#push the images to the local registry

docker tag llm localhost:5000/llmops-llm
docker push localhost:5000/llmops-llm

docker tag embbeding localhost:5000/llmops-embedding
docker push localhost:5000/llmops-embedding

docker tag orchestrator localhost:5000/llmops-orchestrator
docker push localhost:5000/llmops-orchestrator

echo "All images have been built and pushed to the local registry avaible at localhost:5000"