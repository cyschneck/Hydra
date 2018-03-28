#!/bin/bash
echo "Linking repo volume inside of syntaxnet docker container"
echo ""

echo "DOCKER STARTING, entering docker...";
docker run --name mcparseface -v $(pwd)/:/root/models/syntaxnet/Hydra/ --rm -it brianlow/syntaxnet-docker bash
