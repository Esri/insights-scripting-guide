# Insights Scripting Guide

This guide offers a reference for creating custom features in ArcGIS Insights using Python and R.  It covers the mechanics for deploying a Kernel Gateway and other topics about scripting and working with the Insights script editor.

_Note: Scripting is available in Insights Desktop and the ArcGIS Enterprise version of Insights begining at 3.4 and in all 2020+ builds.  Scripting is not available within Insights running in ArcGIS Online._

If you wish to contribute or have questions, please log an issue or create a pull request.


## Setup a Kernel Gateway scripting server

A scripting server is required to create custom tools using Python and R.  Currently, Insights supports connections to Jupyter's Kernel Gateway server.  To learn how to introduce a Kernel Gateway scripting server into your environment read the section on Planning a Scripting Environment.  Then follow the steps in one of these sections: 

* How to deploy a Kernel Gateway using Anaconda
* How to deploy a Kernel Gateway using Docker

_Note: When deploying a Kernel Gateway make sure firewall and port settings permit HTTP connections between Insights and the Kernel Gateway.  For suggestions on how to wire together Insights and Jupyter's Kernel Gateway server (or where to install jupyter software), see section on Options for Planning a Scripting Environment._
   

### How to deploy a Kernel Gateway using Anaconda

Jupyter's Kernel Gateway is a Web Socket and HTTP server which Insights will communicate with to run Python and R code.  Before following the steps in this section, it's reccomended to read the section on Planning a Scipting Environment.

Steps:

1) Install Anaconda 3.7 (or greater)
2) Create a folder named ```gateway```
3) Copy ```selfsign.py``` and ```insights-base.yml``` into your ```gateway``` folder
4) Open the Anaconda command promt and CD into the ```gateway``` folder
5) Run the following commands

``` conda create env -f insights-base.yml ```
``` conda activate insights-base ```
``` python selfsign.py```

Lastly run this command to start Jupyter's Kernel Gateway:

``` jupyter kernelgateway --KernelGatewayApp.ip=0.0.0.0 --KernelGatewayApp.port=9999 --KernelGatewayApp.allow_origin='*' --KernelGatewayApp.allow_credentials='*' --KernelGatewayApp.allow_headers='*' --KernelGatewayApp.allow_methods='*' --JupyterWebsocketPersonality.list_kernels=True --certfile=./server.crt --keyfile=./server.key```


### How to deploy a Kernel Gateway using Docker

Jupyter's Kernel Gateway is a Web Socket and HTTP server which Insights will communicate with to run Python and R code.  Before following the steps in this section, it's reccomended to read the section on Planning a Scipting Environment.


## Planning a Scipting Environment

To help ensure that Insights can communicate with the Kernel Gateway using localhost or a FQDN (fully qualified domain name), this section's purpose is to help determine where to install Jupyter software given your needs and computer network.  To answer this question _where should I deploy a Kernel Gateway_, consider your goals and pick a relevant sub-section to read. 

### _Desktop goal:_

I want to keep things simple and make scripting work on my computer.
Perfect, for this  consider installing Insights Desktop and the Kernel Gateway all on the same computer. 

### _Enterprise goal:_  

My office has ArcGIS Enterprise and Insights running behind our company firewall and I want to enable scripting there.

Ok, for this you consider installing the Kerenl Gateway on a machine that can access your ArcGIS Enterprise and vica-a-versa.  This machine should be on the same network as the ArcGIS Enterprise and have a Fully Qualified Domain Name, ex.  machinename.company.com

### _Cloud Goal:_ 

My ArcGIS Enterprise with Insights is running in a Cloud and I would like to enable scripting.

### _Hybrid Cloud Goal:_

I want scripting server in the Cloud and want to supports connections from ArcGIS Insights running in Enterprise behind a firewall or from Insights Desktop



