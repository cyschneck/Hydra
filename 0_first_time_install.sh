#!/bin/bash
echo "first time install (requires sudo access): docker"
echo ""

sudo apt install docker.io
sudo docker pull brianlow/syntaxnet-docker
sudo groupadd docker
sudo gpasswd -a $USER docker

echo "finished installing docker, only needs to run once"
