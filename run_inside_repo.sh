#!/bin/bash
echo "Copying files to docker container..."
echo ""
docker cp ${PWD}/ mcparseface:/root/models/syntaxnet/Ishmael
echo "done, copied, enter docker to run files"
