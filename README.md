#QGIS Server on docker and rancher

Simple load balanced configuration for QGIS, Rancher and Docker.

This example will host a service with a map of the Winelands District, Western
Cape, South Africa.  Based on data from [OpenStreetMap](openstreetmap.org) and
population data published by [CIESIN](https://ciesin.columbia.edu/data/hrsl/)
with the district boundary provided by [The South African Demarcation
Board](http://www.demarcation.org.za), this is a simple local map of the Cape
Winelands area.

We have made this example public in the hopes that it will inspire others
who are looking for ways to scale up QGIS Server in a production environment.

## Usage:

* Install Rancher server (not covered here)
* Set up a Rancher environment (not covered here)
* Provision at least two hosts into the environment (we used Hetzner CX10 VPS's
  which have 1GB ram, 1x1Ghz CPU - that is probably the minimum you can get away
  with but your published projects may require more oomph...). The supplied
  setup-node.sh script should give you and indication of what is required to
  provision the node. Note that this script if run unmodified will provision your
  host into **our** rancher environment which is definately not what you want, so
  be sure to modify the script.
* Create a new stack in the environment
* Use the docker-compose.yml and rancher-compose.yml provided in this repo to
  start up the service

## Testing:

* Check what IP address your load balancer is running on in rancher web UI.
* Create a new QGIS WMS connection pointing at the load balancer simply in the
  format http://xxx.yyy.zzz.aaa (where xxx.yyy.zzz.aaa is the ip address of your
  load balancer). No need to specify any service descriptors.
* You can also test using the supplied test.sh script which will do two things:
  * run apache benchmark (it assumes it is in your path) against the server
    with two concurrent requests and see how many times it can get a response in
    30s.
  * fetch and open a map request in your preview app (assumes MacOS client) so
    that you can have visual verification that the service works.
 
## How does it work?

We use three containers:

* a loadbalancer (provided by rancher).
* a btsync container that will provide the file store. This will be a rancher
  'sidekick' container meaning that there will always be one sidekick established
  for every QGIS container that gets run. BTSync (now Resilio Sync) provides a
  peer-to-peer file sharing system. With it you can define the files on your
  desktop and they publish to the web without any work on your part. You just
  need to take care on your authoring host to remember that changing a file is
  near immediate and taking drastic action like deleting files locally could have
  bad consequences for the published service. 
* a QGIS container that will publish the maps in the file store.


Note that you will need to adapt this for your own needs since it contains
data that is specific to our company and the test.sh script points to our own
servers.

Tim Sutton
December 2016
