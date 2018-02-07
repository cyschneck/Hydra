#!/bin/bash
echo "Copying files to docker container..."
echo ""

DOCKER_RUNNING=`docker ps -a | grep mcparseface | wc -l`

if [ $DOCKER_RUNNING -eq "0" ]; then
   echo "ERROR: docker is not running, start docker and then restart, exiting";
   echo "run: docker run --name mcparseface --rm -it brianlow/syntaxnet-docker bash";
   exit;
fi

docker cp ${PWD}/ mcparseface:/root/models/syntaxnet/Ishmael
echo "done, copied, enter docker to run files"
