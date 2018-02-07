## Install steps and common errors
1. git clone https://github.com/cschneck/Ishmael.git
2. Install docker for syntaxnet (Parsey), [for more information about Syntaxnet](https://github.com/tensorflow/models/tree/master/research/syntaxnet#installation)
Docker details:
sudo apt install docker.io
sudo docker pull brianlow/syntaxnet-docker
sudo groupadd docker
sudo gpasswd -a $USER docker
docker run --name mcparseface --rm -it brianlow/syntaxnet-docker bash
3. Start process: activate docker with files from repo (new volumnes)
docker run --name mcparseface --rm -it brianlow/syntaxnet-docker bash
4. In new tab (inside original repo): to copy files to docker
./run_inside_repo.sh
5. Inside docker container: to install modules (i.e. vim)
./run_inside_docker_container.sh
