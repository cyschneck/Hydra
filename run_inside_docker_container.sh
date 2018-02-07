#!/bin/bash
echo "install modules needed to run inside docker container..."
echo ""
sed -i -e 's/archive.ubuntu.com\|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
apt-get update
apt-get install vim

