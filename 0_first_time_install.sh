#!/bin/bash
echo "first time install (requires sudo access): docker"
echo ""

echo "apt install docker.io"
sudo apt install docker.io
echo "docker pull brianlow/syntaxnet-docker"
sudo docker pull brianlow/syntaxnet-docker
echo "groupadd docker"
sudo groupadd docker
echo "gpasswd -a $USER docker"
sudo gpasswd -a $USER docker

echo "finished installing docker, only needs to run once"
