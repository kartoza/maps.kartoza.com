#!/bin/bash

# Example to execute
#
# ssh <hostname> 'bash -s' < setup-node.sh


apt-get update
apt-get install -y apt-transport-https ca-certificates
apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list
apt update
apt-cache policy docker-engine
apt-get install -y linux-image-extra-$(uname -r) linux-image-extra-virtual
apt-get install -y docker-engine
service docker start
docker run -d --privileged -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/rancher:/var/lib/rancher rancher/agent:v1.0.2 http://rancher.kartoza.com/v1/scripts/8D9216CE0E07470CECD9:1481526000000:JJQHgxumeNIEx1pQVuR6bIN8glA
apt-get install -y ufw
ufw allow ssh
ufw allow http
ufw allow https
ufw default deny incoming
ufw enable
# Note docker will automatically punch a hole through iptables
# for any service where you have mapped a public port
# see http://blog.viktorpetersson.com/post/101707677489/the-dangers-of-ufw-docker

# Prefetch these images to make startup quicker
docker pull kartoza/btsync
docker pull kartoza/qgis-server:2.14
