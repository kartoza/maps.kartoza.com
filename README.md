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
* Create a new stack in the environment (illustrated in screenshots below)
* Use the docker-compose.yml and rancher-compose.yml provided in this repo to
  start up the service (illustrated below)
  
  
Adding a new stack...

![screen shot 2016-12-12 at 3 10 29 pm](https://cloud.githubusercontent.com/assets/178003/21100546/55107158-c07d-11e6-841c-ffca92b583c9.png)

Setting the docker-compose and rancher-compose yaml files...

![screen shot 2016-12-12 at 3 11 02 pm](https://cloud.githubusercontent.com/assets/178003/21100547/57e910ce-c07d-11e6-9645-4379435e5724.png)

Waiting for the stack to spin up...
![screen shot 2016-12-12 at 3 12 16 pm](https://cloud.githubusercontent.com/assets/178003/21100561/6d93197e-c07d-11e6-968a-d86fecaa9a3b.png)


Stack spin up completed...
![screen shot 2016-12-12 at 3 15 33 pm](https://cloud.githubusercontent.com/assets/178003/21101144/6d00028a-c080-11e6-9457-3757fea16b6d.png)


QGIS Nodes (currently 2 running)...
![screen shot 2016-12-12 at 3 15 53 pm](https://cloud.githubusercontent.com/assets/178003/21101148/7431a0ea-c080-11e6-89de-edaba6d9a6e1.png)

Detailed view of nodes ...
![screen shot 2016-12-12 at 3 16 33 pm](https://cloud.githubusercontent.com/assets/178003/21101209/b992c4c0-c080-11e6-9541-344446dea3c4.png)


Provisioning a new host ...
![screen shot 2016-12-12 at 3 17 05 pm](https://cloud.githubusercontent.com/assets/178003/21101216/c2d35ce8-c080-11e6-9845-ad4342f80bd7.png)


Scaling up to three nodes ...
![screen shot 2016-12-12 at 3 32 12 pm](https://cloud.githubusercontent.com/assets/178003/21101224/c886bfe0-c080-11e6-884a-a7db06a6d35b.png)

Waiting while a new node spins up ...
![screen shot 2016-12-12 at 3 32 22 pm](https://cloud.githubusercontent.com/assets/178003/21101232/cd3fe534-c080-11e6-9f63-020d6e5f47d7.png)

Third node integrated into the stack ...
![screen shot 2016-12-12 at 3 33 15 pm](https://cloud.githubusercontent.com/assets/178003/21101236/d4746d0c-c080-11e6-9578-c94ee9402a92.png)



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

 Here is a sample output for two nodes:
 
 ```
 Concurrency Level:      2
Time taken for tests:   34.177 seconds
Complete requests:      3
Failed requests:        0
Total transferred:      30558 bytes
HTML transferred:       30090 bytes
Requests per second:    0.09 [#/sec] (mean)
Time per request:       22784.397 [ms] (mean)
Time per request:       11392.198 [ms] (mean, across all concurrent requests)
Transfer rate:          0.87 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:      215  222  13.0    226     237
Processing: 15198 17344 1861.9  18417   18527
Waiting:    15170 17319 1864.9  18394   18511
Total:      15435 17566 1848.9  18631   18742
```

And here is what happens if we scale up to three nodes and then rerun the test:

```
Concurrency Level:      2
Time taken for tests:   37.368 seconds
Complete requests:      5
Failed requests:        0
Total transferred:      50930 bytes
HTML transferred:       50150 bytes
Requests per second:    0.13 [#/sec] (mean)
Time per request:       14947.096 [ms] (mean)
Time per request:       7473.548 [ms] (mean, across all concurrent requests)
Transfer rate:          1.33 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:      202  253  45.5    273     300
Processing: 12124 13057 1470.0  12712   15594
Waiting:    12112 13050 1471.5  12711   15588
Total:      12343 13310 1491.5  12944   15893
```

You can see that in particular the time per request dropped from 11.4 seconds 
to 7.5 seconds by adding one node. You can also in rancher the load being 
spread nicely across the nodes:

![screen shot 2016-12-12 at 4 26 10 pm](https://cloud.githubusercontent.com/assets/178003/21102952/0f1a8c0e-c089-11e6-8076-77dcbd8f8159.png)

Here you can see the load balancer spreading the requests as I do many sequential
map interactions in QGIS (using it as a WMS client). The screencapture below switches 
between rancher to show CPU and IO load and the QGIS desktop.

![qgis](https://cloud.githubusercontent.com/assets/178003/21103728/5596a070-c08c-11e6-8b60-e102983ff130.gif)

## Caveats

1. Note that you will need to adapt this for your own needs since it contains
  data that is specific to our company and the test.sh script points to our own
  servers.
1. When spinning up a new node, it may return OGC service errors until the btsync 
  is completed. I don't have an elegant way to deal with this (yet) so you should 
  take that into consideration both when testing and trying to understand if things 
  are working, and in production as you load balancer may start forwarding traffic 
  to the new node before it is actually ready to respond to these requests.


Tim Sutton
December 2016
