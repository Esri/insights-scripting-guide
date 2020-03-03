# Insights Scripting Guide

This guide offers a reference for creating custom features in ArcGIS Insights using Python and R.  It is the definitive guide for Insights scripting topics and a resource for implementing Jupyter's Kernel Gateway.
 

## Prerequisites

* ArcGIS Insights (version 2020.x)
* Anaconda (version 3.7)
* See needed Python and R [dependencies](gateway/insights-base.yml) 

_Note: Insights in ArcGIS Online does not support scripting.  Please use Insights Desktop until this becomes a supported feature._ 


## Kernel Gateway Setup 

Insights supports connections to Jupyter's Kernel Gateway version 2.1.0, which is an open source web server distributed through ```conda-forge``` and other channels.  To learn how to setup a Kernel Gateway with the required dependencies choose one of the following deployment sections.

* [How to deploy a Kernel Gateway with dependencies using Anaconda](#How-to-deploy-a-Kernel-Gateway-with-dependencies-using-Anaconda)
* [How to deploy a Kernel Gateway with dependencies using Docker](#How-to-deploy-a-Kernel-Gateway-with-dependencies-using-Docker)

Insights Desktop readers should review [How to deploy a Kernel Gateway for Insights Desktop](How-to-deploy-a-Kernel-Gateway-for-Insights-Desktop). 

### How to deploy a Kernel Gateway with Anaconda

It's reccomended to read [Planning a Scipting Environment](#Planning-a-Scripting-Environment) before following these steps.

1) Install [Anaconda v3.7](https://www.anaconda.com/distribution/#download-section)
2) Create a folder named ```gateway```
3) Copy ```selfsign.py``` and ```insights-base.yml``` into ```gateway``` folder
4) Open _Anaconda's command promt_ and CD into the ```gateway``` folder
5) Run below commands

    ```
    conda env create -f insights-base.yml
    conda activate insights-base
    python selfsign.py
    ```

6) Start the Kernel Gateway:

* Run this command if using __Insights in ArcGIS Enterprise__

    ```
    jupyter kernelgateway --KernelGatewayApp.ip=0.0.0.0 --KernelGatewayApp.port=9999 --KernelGatewayApp.allow_origin='*' --KernelGatewayApp.allow_credentials='*' --KernelGatewayApp.allow_headers='*' --KernelGatewayApp.allow_methods='*' --JupyterWebsocketPersonality.list_kernels=True --certfile=./server.crt --keyfile=./server.key
    ```

* Run this command if using __Insights Desktop__

    ```
    jupyter kernelgateway --KernelGatewayApp.ip=0.0.0.0 --KernelGatewayApp.port=9999 --KernelGatewayApp.allow_origin='*' --KernelGatewayApp.allow_credentials='*' --KernelGatewayApp.allow_headers='*' --KernelGatewayApp.allow_methods='*' --JupyterWebsocketPersonality.list_kernels=True
    ```

7) _Optional:_  Stop Kernel Gateway by pressing _Control-C_ in the running window or close the window



### How to deploy a Kernel Gateway with dependencies using Docker

...Coming soon...


## Create a connection

To create a Jupyter Kernel Gateway connection complete the Kernel Gateway Connection form. 


1) Open Insights
2) Click the _Scripting_ icon 
3) Complete Kernel Gateway Connection form


![Scripting Icon](diagrams/scripting_icon.png)



![Kernel Gateway Connection](diagrams/connection.png)


_Note:_  This form needs the root URL of your Kernel Gateway.  For tips on choosing the correct URL schema, it's reccomended to read [Kernel Gateway URL Patterns](#Kernel-Gateway-URL-Patterns).  


## Kernel Gateway URL Patterns


| URL           | Insights in Enterprise | Insights Desktop  |
| ------------- |:-------------:| -----:|
| http://localhost:9999      | no | yes |
| https://localhost:9999      | no      |   no |
| http://pickle:9999| no      |    yes |
| https://pickle:9999| no      |    no |
| http://12.120.95.153:9999 | no      |    yes |
| https://12.120.95.153:9999| yes      |    no |
| http://pickle.esri.com:9999| no      |    yes |
| https://pickle.esri.com:9999| yes      |    no <sup>1</sup> |

<sup>1</sup> Insights Desktop can make connections to HTTPS Kernel Gateway endpoints, if the Kernel Gateway uses a domain or a certificate authority certificate.




## General Features

Python and R scripting features are distributed across the app.  Shared scripts can be accessed from the _Add_ dialog, script  modules are accessed via the data pane and the editor console has many features.  Refer to this table for an overview of scripting tool. 

| Icon           | Tool Name | Description  |
| :-------------: |:-------------:| :-----|
| ![Open console](diagrams/scripting-console.svg)      | Open console | Opens the Python and R scripting console or Kernel Gateway connection dialog. If no Kernel Gateway connection exists within the page, this is when the connection dialog openes. |
| ![Create module](diagrams/add-model.svg)     | Create module      |   Creates a script from selected cells then adds a module to the data pane. |
| ![Create card](diagrams/create-card.svg)| Create card      |    Takes the active cell and creates a card. |
| ![Delete cell](diagrams/delete-cell.svg)| Delete cell      |    Deletes the active cell. |
| ![Export script](diagrams/export-save.svg) | Export script      |    Enables saving of cell (or cells) to common formats like Python, R, or Jupyter Notebook files. |
| ![Import file](diagrams/import-file.svg) | Import file      |    Enables importing of scripts into the console from common files like Python, R or Jupyter Notebook files. |
| ![Insert cell](diagrams/insert-cell.svg) | Insert cell      |    Inserts a new scripting cell. |
| ![Restart kernel](diagrams/restart.svg)| Restart kernel      |    Restarts the execution kernel within the Kernel Gateway.  Restarting stops running scripts and clears the namespace and any data held in memory.  |
| ![Run](diagrams/run.svg)| Run  | Runs script in active cell. |
| ![Run all](diagrams/run-all.svg) |    Run all  | Runs all scripts in active cell. |
| ![Switch connection](diagrams/switch-connections.svg)| Switch connection      |    Enables connection changing from one Kernel Gateway to another.  |


### Shortcuts

The console enables keyboard shortcuts to perform routine tasks quickly.

| Shortcut           | Description |
|:-------------:|:-------------:|
| _Ctrl + B_     | Create comments for selected code. |
| _Shift + Enter_      | Executes code in current cell. |
| _Ctrl + Alt + B         | Adds ```%insights_return(<data frame object>)``` magic command to cell  |


### Magic commands

The console supports the following magic command.  This magic command must be placed in it's own cell.

| Magic command           | Description |
|:-------------:|:-------------:|
| ```%insights_return(<data frame object>)```     | Converts Python or R data frames into Insights datasets.  When ```%insights_return(df)```  is run it will generate an Insights dataset from the ```df``` object.  Data will be persisted in the workbook (when the workbook is saved) and will appear in the data pane after execution.  |


## Planning a Scipting Environment

There are various configurations to choose from when planning a Jupyter Kernel Gateway deployment.  It should be noted that some configurations make have a tactical advantage over others.  Additionally, each configuration will offer different end-user experiences and varying degress of effort in regards to deployment and maintence.

These conceptual diagrams were designed to help organizations visualize different Jupyter Kernel Gateway configurations. 

### Insights Desktop and Kernel Gateway

![Insights Desktop and Kernel Gateway](diagrams/jkg-desktop-diagram.png)


* This configuration entails low newtworking and firewall considerations
* Data files may live on personal computer or file server


### Insights in ArcGIS Enterprise and Kernel Gateway  

#### Dedicated

![Dedicated Kernel Gateway](diagrams/jkg-dedicated-diagram.png)

* This configuration entails moderate newtworking and firewall considerations and skills
* Data files should live on file server or Kernel Gateway machine


#### Co-Located

![Co-Located Kernel Gateway](diagrams/jkg-colocated-diagram.png)

* This configuration entails moderate newtworking and firewall considerations and skills
* Data files should live on file server or Kernel Gateway machine


#### Client Kernel Gateway System Design

![Client Kernel Gateway](diagrams/jkg-client-diagram.png)

* This configuration entails moderate newtworking and firewall considerations and skills
* Data files may live on personal computer or file server



### Cloud Kernel Gateway 

* Data files may need to be accessible from the cloud
* This configuration entails advanced newtworking and firewall skills and considerations

![Cloud Kernel Gateway](diagrams/jkg-cloud-diagram.png)



## Troubleshooting 

_Insights is running in the web browser and when connecting to a Kernel Gateway an error says "Not able to add this connection. Try with a different URL or web socket or check if your gateway is running."_

If you've followed the guide (and ran the selfsign.py file), you have created a self signed SSL certificate. It may be possible that Insights cannot make a connection because the web browser itself does not trust the certificate. To work around this problem open the kernel gateway URL in the web browser and accept the browser warning. Then try connecting again.



_My Kernel Gateway is on a different machine and I am having trouble making a connection using Insights?_

A fundemental way to toubleshoot this problem is confirm that all needed computers can talk to each other.   If you are running Insights in Enterprise this means each ArcGIS Server machine, plus your Kernel Gateway and personal computer must all be able to communicate with each other.   Insights Desktop entails less troubleshooting.  For Insights Desktop only the Kernel Gateway and your personal computer need to talk to each other.

 Try getting the IP address of:
 
 * Your personal computer machine
 * Your kernel gateway machine
 * Your ArcGIS Server machine(s) 
 
 and then from each machine run the ```ping``` command to see if ping messages are received. 

Tip:  On windows, run ```ipconfig``` and reference the Iv4 address to get the IP address.  On mac, run ```ipconfig getifaddr en0``` and note the address.  


## Contribute

If you wish to contribute or have questions, please create an issue or pull request.


## Start using ArcGIS Insights with a Free Trial

Sign-up to [start a free trial](https://www.esri.com/en-us/arcgis/products/insights-for-arcgis/trial?adumkts=product&adupro=Insights_for_ArcGIS&aduc=pr&adum=blogs&utm_Source=pr&aduca=arcgis_insights_existing_customers_promotions&aduat=blog&aduco=exploring-the-atlantic-ocean-in-insights&adupt=lead_gen&sf_id=70139000001eKGfAAM).


## Licensing
Copyright 2020 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the license is available in the repository's [license.txt]( https://raw.github.com/Esri/quickstart-map-js/master/license.txt) file.
