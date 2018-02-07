## Install steps and common errors
1. git clone https://github.com/cschneck/Ishmael.git
2. If first time setup:

```./0_first_time_install.sh ```

3. To run docker image:

Once docker has been installed (via 0_first_time_install.sh or manually), start docker container 'mcparseface'

```docker run --name mcparseface --rm -it brianlow/syntaxnet-docker bash```

4. In new tab (open within cloned repo Ishmael): clone repo into docker container

```./1_run_inside_repo.sh```

5. Within the open docker container: install modules to run python scripts

```./2_run_inside_docker_container.sh```
