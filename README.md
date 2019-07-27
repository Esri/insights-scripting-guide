# Insights scripting guide - _Beta release_

Welcome to the Insights scripting guide.

This repo contains information on getting started with scripting in Insights. The Beta Release enables the execution of Python and R code using a bring-your-own scripting environment. Among many topics, we outline how to deploy a Jupyter Kernel Gateway, how to connect to a Jupyter Kernel Gateway, and tips and tricks for using the Insights scripting environment with other Insights features. In addition, the repo serves as a place to find and share useful Python and R scripts and creates a community around those who prefer to write code to advance data science and knowledge sharing.

We welcome any contributions for improving this guide. If you find a bug or would like to report a problem in the Beta release of the Insights scripting environment, please log an issue in this repo.

## Overview

* Learn how to configure a Jupyter Kernel Gateway (this is a requirement for using the Insights scripting environment).
* Pick a [Windows](#windows-instructions) or [macOS](#macos-instructions) machine, such as a desktop or laptop, to host your Jupyter Kernel Gateway.
* Generate Transport Layer Security (TLS) or Secure Sockets Layer (SSL) certificates.
* Follow the guide for installing and deploying a Jupyter Kernel Gateway.
* Learn tips about keyboard shortcuts and important scripting options.
* Search for Python and R code.
* Contribute Python and R code.
* Read Insights use cases and product documentation.
* Try Insights in Enterprise.
* Use the Insights scripting environment in Enterprise.  


### Client data limitations
The following limitations exist for the Insights scripting environment. These limitations are temporary during the Beta release and will be removed once the Insights scripting environment is out of Beta.
In the Beta Release, there are limitations on the size of data that can be exported from the Insights scripting environment to the Insights data pane. These limitations do not exist when bringing data from the Insights data pane into the Insights scripting environment. These limitations are temporary during the Beta Release and will be removed once the Insights scripting environment is out of Beta.
* Exporting data from the Insights scripting environment to the Insights data pane.
  * Current limit of ~ 8 MB for data frame size.
  * ~ 27000 rows X 10 columns of mixed data types.


### Required packages to export data from the scripting environment to the data pane
To export data from the Insights scripting environment to the Insights data pane, the following Python and R packages are used:
* The Python Kernel uses ```pandas```, ```GeoPandas```, and ```NumPy```.
* The R Kernel uses ```jsonlite```, ```data.table```, and ```itertools```.

Insights will install these packages if they are not available in the respective kernels. 


## Install and deploy a Jupyter Kernel Gateway

The Insights scripting environment uses a Jupyter Kernel Gateway. This section includes guidance on how to configure a Jupyter Kernel Gateway. It requires using either Docker or Anaconda and enabling TLS or SSL for security. TLS and SSL permit Insights to access your gateway over HTTPS and WSS.

## Windows instructions

### Create a TLS or SSL certificate

1) Clone the insights-scripting-guide repo to your local machine.
2) Use [Anaconda](https://www.anaconda.com/distribution/#windows) to install ``` openssl ``` for creating a self-signed certificate.
3) Open the Anaconda Command Prompt window. 
4) Create a folder called __insightsgw__ on your local machine. For example, ``` C:\insightsgw ```.
5) Copy and paste the __insightsgw.cnf__ file from this repo's __Cert__ folder into the __insightsgw__ folder and edit each placeholder value (__host_name__ and __domain__) within the file.
  
Example:

``` 
[dn]
CN=insights.esri.com
[req]
distinguished_name=dn
[EXT]
subjectAltName=DNS:insights.esri.com
keyUsage=digitalSignature
extendedKeyUsage=serverAuth
```

> When editing the __insightsgw.cnf__ file, if you are unsure of your __host_name__ run ``` hostname ``` from a command prompt to get the correct value. If you are unsure of your __domain__ run ``` set user ``` from a command prompt to get the correct value.

6) Using the Anaconda Command Prompt, change directories to __insightsgw__. For example, ``` cd C:\insightsgw ```.
7) Change the placeholders for __<host_name>__ and __<dns_name>__ and run the following command:

``` openssl req -x509 -days 365 -out <host_name>.crt -keyout <host_name>.key -newkey rsa:2048 -nodes -sha256 -subj "/CN=<host_name>.<dns_name>" -extensions EXT -config insightsgw.cnf ```

Example:

``` openssl req -x509 -days 365 -out insights.crt -keyout insights.key -newkey rsa:2048 -nodes -sha256 -subj "/CN=insights.esri.com" -extensions EXT -config insightsgw.cnf ```

8) Close the Anaconda Command Prompt when the command has finished running. There should now be a __<host_name>.key__ and a __<host_name>.crt__ file in your __insightsgw__ folder.
9) Using administrative privileges, import the .crt file in your __insightsgw__ folder into the Windows Certificate Store's Trusted Root Certification Authorities. Use the following steps:
   * Open Manage computer certificates.
   * Open Trusted Root Certification Authorities.
   * Right click Certificates.
   * Click All Tasks > Import.
   * Select the .crt file created using ``` openssl ```.
   * Flush DNS using by running ```ipconfig /flushdns``` from the command prompt.
10) Add new _Inbound_ and _Outbound_ rules for port 9999 using Windows Defender Firewall with Advanced Security. 

### Create a gateway

_When creating a Jupyter Kernel Gateway choose either the Docker or Anaconda section below (not both)._

#### Create a gateway using Docker

1) Install [Docker](https://www.docker.com/products/docker-desktop).
2) Create a folder called __insightsgw__ on your local machine for example, ``` c:\insightsgw ```.
3) Copy and paste ``` Dockerfile ``` from this repo's _Docker_ folder into the __insightsgw__ folder.
4) Edit ``` Dockerfile ``` to fit your requirements.

> The ENV KG_ALLOW_ORIGIN and ENV KG_LIST_KERNELS parameters are required for the Jupyter Kernel Gateway

> If you want to load data into the container to work with inside the Insights console, create a local folder and add the data files to it and then set that folder to be copied from the local machine to the container in the ```Dockerfile```. For example, create a folder in your local project folder __insightsgw__ named __data__ and add working data files to it. Then, add ```COPY /data/* /data/``` to the ```Dockerfile``` to copy the local __data__ folder with the files to the container. Adding ```WORKDIR /data``` to the ```Dockerfile``` will set the container working folder to the __data__ folder.

5) Run ``` docker build -t insightsgw . ``` from a command prompt in the folder created in step 2. For example, ``` c:\insightsgw>docker build -t insightsgw . ```
6) Run ``` docker run -p 9999:9999 insightsgw ``` from a command prompt in the folder created in step 2. For example, ``` c:\insightsgw>docker run -p 9999:9999 insightsgw ```

> If there is a database on the local host machine with data to be used in the Insights console, a connection to it can be created in the docker run command. For example, connecting to PostgreSQL in Windows ``` docker run -p 9999:9999 -e DB_PORT=5432 -e DB_HOST=docker.for.win.host.internal insightsgw ```

&nbsp;&nbsp;&nbsp;&nbsp;Upon success the prompt will show the following output: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``` [KernelGatewayApp] Jupyter Kernel Gateway at https://0.0.0.0:9999 ```

7) Leave the command prompt open while the Jupyter Kernel Gateway is running.
8) To test that the gateway is running as expected, open a web browser and navigate to ``` https://<host_name>.<dns_domain>:9999/api ```. For example, https://insights.esri.com:9999/api.  

&nbsp;&nbsp;&nbsp;&nbsp;You should see JSON text on the web page showing the api version information. For example, 
``` {"version": "5.7.4"} ```.

> The default configuration of Docker is limiting so it is best practice to use Docker's Advanced Setting tab to configure additional CPU and memory resources.

> In addition to configuring resources for the container from the Docker application, they can be configured within ``` Dockerfile ``` as well. See the Docker documentation for configuration details.

#### Create a gateway using Anaconda

1) Install [Anaconda](https://www.anaconda.com/distribution/).
2) Open the Anaconda Command Prompt window.
3) Create an Insights Python environment using the command ``` conda create -n my_insights_env python=3.6 ```.
4) Activate the insights Python environment using the command ``` conda activate my_insights_env ```.
5) Install Jupyter Kernel Gateway using the command ``` conda install -c anaconda jupyter_kernel_gateway=2.1.0```.
6) Install pandas, GeoPandas, and NumPy packages along with any other packages you require using the command ``` conda install -c anaconda numpy pandas geopandas```.
7) Add the ArcGIS API for Python using the command ``` conda install -c esri arcgis ```.
8) Install essential R packages using the command ``` conda install -c r r-essentials ```.
9) Add the itertools package using the command ``` conda install -c conda-forge r-itertools ```.

> Consider what directory to use when launching the Jupyter Kernel Gateway. If you have a ``` C:\insightsgw\data ``` directory which contains ``` .csv ``` files, launching the Jupyter Kernel Gateway from this folder will enable easy access to those files within scripts by allowing the use of relative paths for file and folder access.

> The ``` KernelGatewayApp.allow_origin ``` and ``` JupyterWebsocketPersonality.list_kernels ``` parameters are required.

10) Launch the Jupyter Kernel Gateway using the following command, changing the placeholders for __<host_name>__
``` 
jupyter kernelgateway --KernelGatewayApp.ip=0.0.0.0 --KernelGatewayApp.port=9999 --KernelGatewayApp.allow_origin='*' --KernelGatewayApp.allow_credentials='*' --KernelGatewayApp.allow_headers='*' --KernelGatewayApp.allow_methods='*' --JupyterWebsocketPersonality.list_kernels=True --certfile=C:\insightsgw\<host_name>.crt --keyfile=C:\insightsgw\<host_name>.key 
```

Example:

``` 
jupyter kernelgateway --KernelGatewayApp.ip=0.0.0.0 --KernelGatewayApp.port=9999 --KernelGatewayApp.allow_origin='*' --KernelGatewayApp.allow_credentials='*' --KernelGatewayApp.allow_headers='*' --KernelGatewayApp.allow_methods='*' --JupyterWebsocketPersonality.list_kernels=True --certfile=C:\insightsgw\insights.crt --keyfile=C:\insightsgw\insights.key 
```
&nbsp;&nbsp;&nbsp;&nbsp;Upon success the prompt will show the following output: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``` [KernelGatewayApp] Jupyter Kernel Gateway at https://0.0.0.0:9999 ```

11) Leave the command prompt open while the Jupyter Kernel Gateway is running.

12) To test that the Gateway is running as expected, open a web browser and navigate to ``` https://<host_name>.<dns_domain>:9999/api ```. For example, https://insights.esri.com:9999/api.

&nbsp;&nbsp;&nbsp;&nbsp;You should see JSON text on the web page showing the api version information. For example, 
``` {"version": "5.7.4"} ```.

> If you are experiencing issues connecting to the console after creating a self-signed certificate, check the browser to make sure an exception does not need to be added for the site created in the certificate. In the example above, the site is ``` https://insights.esri.com ```. Navigate to ``` https://insights.esri.com ``` in the browser. If an exception is required for the self-signed certificate, a warning page will be shown:

> <img src="/Graphics/cert_excep.png" />

> Click Advanced

> <img src="/Graphics/cert_excep_add.png" />

> Click Add Exception...

> <img src="/Graphics/cert_excep_conf.png" />

> Click Confirm Security Exception

## macOS instructions

### Create a TLS or SSL cert

1) Clone the insights-scripting-guide repo to your local machine.
2) Create a directory called __insightsgw__ on your local machine. For example, ``` insightspc:insightsgw insightsuser$  ```.
3) Copy and paste the __insightsgw.cnf__ file from this repo's __Cert__ directory into the __insightsgw__ directory and edit each placeholder value (__host_name__ and __domain__)  within the file.

Example:

``` 
[dn]
CN=insights.esri.com
[req]
distinguished_name=dn
[EXT]
subjectAltName=DNS:insights.esri.com
keyUsage=digitalSignature
extendedKeyUsage=serverAuth
```

> When editing the __insightsgw.cnf__ file, if you are unsure of your __host_name__ run ``` sudo scutil --get LocalHostName ``` from the terminal to get the correct value. If you are unsure of your __domain__ run ``` sudo scutil --get HostName ``` from the terminal to get the correct value.

4) Using the terminal, change directories to __insightsgw__. For example, ``` insightspc:Documents insightsuser$ cd insightsgw ```.

&nbsp;&nbsp;&nbsp;&nbsp;``` openssl ``` is installed on macOS by default.

5) Change the placeholders for __<host_name>__ and __<dns_name>__ and run the following command: 

``` openssl req -x509 -days 365 -out <host_name>.crt -keyout <host_name>.key -newkey rsa:2048 -nodes -sha256 -subj '/CN=<host_name>.<dns_name>' -extensions EXT -config ../insightsgw.cnf ```

Example:

``` openssl req -x509 -days 365 -out insights.crt -keyout insights.key -newkey rsa:2048 -nodes -sha256 -subj '/CN=insights.esri.com' -extensions EXT -config ../insightsgw.cnf ```

&nbsp;&nbsp;&nbsp;&nbsp;The terminal can be closed when finished.

&nbsp;&nbsp;&nbsp;&nbsp;There should now be a __<host_name>.key__ and a __<host_name>.crt__ file in your __insightsgw__ directory.

6) Using administrative privileges, import the .crt file in your __insightsgw__ directory into the Mac Keychain. Use the following steps:
   * Open Keychain
   * Choose System from Keychains
   * Choose Certificates from Category
   * Click File > Import Items
   * Choose ```.crt``` file created using ```openssl```
   * Flush the DNS using ```sudo killall -HUP mDNSResponder``` from terminal

### Create a gateway

_When creating a Jupyter Kernel Gateway choose either the Docker or Anaconda section below (not both)._

#### Create a gateway using Docker

1) Install [Docker](https://www.docker.com/products/docker-desktop).
2) Create a directory called __insightsgw__ on your local machine. For example, ``` insightspc:insightsgw insightsuser$ ```.
3) Copy and paste ``` Dockerfile ``` from this repo's __Docker__ directory into the __insightsgw__ directory.
4) Edit ``` Dockerfile ``` to fit your requirements.

> The ENV KG_ALLOW_ORIGIN and ENV KG_LIST_KERNELS parameters are required for the Jupyter Kernel Gateway.

> If you want to load data into the container to work with inside the Insights console, create a local directory and add the data files to it and then set that directory to be copied from the local machine to the container in ```Dockerfile```. For example, create a directory in your local project directory __insightsgw__ named __data__ and add working data files to it. Then, add ```COPY /data/* /data/``` to ```Dockerfile``` to copy the local __data__ directory with the files to the container. Adding ```WORKDIR /data``` to ```Dockerfile``` will set the container working directory to the __data__ directory.
5) Run ``` docker build -t insightsgw . ``` from the terminal in the directory created in step 2. For example, ```insightspc:insightsgw insightsuser$docker build -t insightsgw . ```
6) Run ``` docker run -p 9999:9999 insightsgw ``` from the terminal in the folder created in step 2. For example, ``` insightspc:insightsgw insightsuser$docker run -p 9999:9999 insightsgw  ```

&nbsp;&nbsp;&nbsp;&nbsp;Upon success the prompt will show the following output: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``` [KernelGatewayApp] Jupyter Kernel Gateway at https://0.0.0.0:9999 ```

&nbsp;&nbsp;&nbsp;&nbsp;Leave the terminal open while the Jupyter Kernel Gateway is running.

7) To test that the Gateway is running as expected, open a web browser and navigate to ``` https://<host_name>.<dns_domain>:9999/api ```. For example, https://insights.esri.com:9999/api.  
&nbsp;&nbsp;&nbsp;&nbsp;You should see JSON text on the web page showing the api version information. For example, 
``` {"version": "5.7.4"} ```.

> The default configuration of Docker is limiting so it is highly recommended to use Docker's Advanced Setting tab to configure additional CPU and memory resources.

> In addition to configuring resources for the container from the Docker application, they can be configured within the Dockerfile as well. See the Docker documentation for configuration details.

#### Create a gateway using Anaconda

1) Install [Anaconda](https://www.anaconda.com/distribution/).
2) Open the terminal window.
3) Create an Insights Python environment using the command ``` conda create -n my_insights_env python=3.6 ```.
4) Activate the insights Python environment using the command ``` source activate my_insights_env ```.
5) Install Jupyter Kernel Gateway using the command ``` conda install -c anaconda jupyter_kernel_gateway ```.
6) Install pandas and NumPy packages along with any other packages you require using the command ``` conda install -c anaconda numpy pandas ```.
7) Add the ArcGIS API for Python using the command ``` conda install -c esri arcgis ```.
8) Install essential R packages using the command ``` conda install -c r r-essentials ```.
9) Add the itertools package using the command ``` conda install -c conda-forge r-itertools ```.

> Consider what directory to use when launching the Jupyter Kernel Gateway. If you have a ``` /Users/insightsuser/Documents/insightsgw/data ``` directory which contains ``` .csv ``` files, launching the Jupyter Kernel Gateway from this directory will enable easy access to those files within scripts by allowing the use of relative paths for file and directory access.

> The ``` KernelGatewayApp.allow_origin ``` and ``` JupyterWebsocketPersonality.list_kernels ``` parameters are required.

10) Launch the Jupyter Kernel Gateway using the following command, changing the placeholders for __<host_name>__
``` 
jupyter kernelgateway --KernelGatewayApp.ip=0.0.0.0 --KernelGatewayApp.port=9999 --KernelGatewayApp.allow_origin='*' --KernelGatewayApp.allow_credentials='*' --KernelGatewayApp.allow_headers='*' --KernelGatewayApp.allow_methods='*' --JupyterWebsocketPersonality.list_kernels=True --certfile=../certs/<host_name>.crt --keyfile=../certs/<host_name>.key
```

Example:

```
jupyter kernelgateway --KernelGatewayApp.ip=0.0.0.0 --KernelGatewayApp.port=9999 --KernelGatewayApp.allow_origin='*' --KernelGatewayApp.allow_credentials='*' --KernelGatewayApp.allow_headers='*' --KernelGatewayApp.allow_methods='*' --JupyterWebsocketPersonality.list_kernels=True --certfile=../certs/insights.crt --keyfile=../certs/insights.key
```
&nbsp;&nbsp;&nbsp;&nbsp;Upon success the prompt will show the following output: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``` [KernelGatewayApp] Jupyter Kernel Gateway at https://0.0.0.0:9999 ```

&nbsp;&nbsp;&nbsp;&nbsp;Leave the terminal open while the Jupyter Kernel Gateway is running.

11) To test that the gateway is running as expected, open a web browser and navigate to ``` https://<host_name>.<dns_domain>:9999/api ```. For example,  https://insights.esri.com:9999/api.

14) You should see JSON text on the web page showing the api version information. For example, 
``` {"version": "5.7.4"} ```

> If you are experiencing issues connecting to the console after creating a self-signed certificate, check the browser to make sure an exception does not need to be added for the site created in the certificate. In the example above, the site is ``` https://insights.esri.com ```. Navigate to ``` https://insights.esri.com ``` in the browser. If an exception is required for the self-signed certificate, a warning page will be shown:

> <img src="/Graphics/cert_excep.png" />

> Click Advanced

> <img src="/Graphics/cert_excep_add.png" />

> Click Add Exception...

> <img src="/Graphics/cert_excep_conf.png" />

> Click Confirm Security Exception

## Use the console in Insights

The Insights Console is available within workbooks only in the Enterprise version, not in Online. You can launch the console by clicking the _Console_ button <img src="/Graphics/console_16.png" />  next to the _Basemap_ button in the workbook toolbar.

Learn more about the scripting console in the Insights documentation.

### Connecting your Jupyter Kernel Gateway

1) To connect Insights to your Jupyter Kernel Gateway, click the _Console_ button <img src="/Graphics/console_16.png" />.

&nbsp;&nbsp;&nbsp;&nbsp;The New Jupyter Kernel Gateway connection window opens.

2) Enter the URL and web socket connection information.

&nbsp;&nbsp;&nbsp;&nbsp;If using the examples in this guide, the __URL__ parameter will be ``` https://<host_name>.<dns_domain>:9999 ``` and the __Web socket__ parameter will be ``` wss://<host_name>.<dns_domain>:9999 ```.
  
Example:

  * URL
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```https://insights.esri.com:9999```
  
  * Web Socket
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```wss://insights.esri.com:9999```
  
### Shortcuts and Insights magic commands

The Insights console uses keyboard shortcuts and magic commands so that routine tasks can be performed quickly and efficiently.
* Use the ```%insights_return(<R data frame or Pandas DataFrame>)``` magic command to add an R data frame or Pandas DataFrame to the Insights data pane.

&nbsp;&nbsp;&nbsp;&nbsp;__The %insights_return magic command must be run on a single line in a single cell in the Insights Console__

* ``` Ctrl/control + Alt/option + B ``` Add ```%insights_return``` magic command to cell.
* ``` Ctrl/control + / ``` Comment line.
* ``` Ctrl/control + Spacebar ``` Enable IntelliSense.
* ``` Shift/shift + Enter/return ``` Execute the code in the current cell.
* ``` Shift/shift + Up Arrow or Down Arrow ``` Access the history of executed cells.

# What is Insights for ArcGIS?

Part of the Esri Geospatial Cloud, Insights for ArcGIS is web-based data analytics made for advanced location intelligence. Answer questions you didn’t know to ask, analyze data completely, and tell powerful data stories. Connect to your data directly, then use maps, charts and tables to perform basic to complex analyses that scale based on skill level and business need.

* [Case studies and testimonials](https://www.esri.com/en-us/arcgis/products/insights-for-arcgis/overview)
* [Product and analytical tool documentation](https://doc.arcgis.com/en/insights/)


## Why Get Involved?

Send feedback to us concerning the Beta Release of the Insights scripting console. Found an issue or have questions? Feel free to post questions or comments and report bugs to the issues section of this repo.

## Start using Insights for ArcGIS with a Free Trial

Sign-up to [start a free trial](https://www.esri.com/en-us/arcgis/products/insights-for-arcgis/trial?adumkts=product&adupro=Insights_for_ArcGIS&aduc=pr&adum=blogs&utm_Source=pr&aduca=arcgis_insights_existing_customers_promotions&aduat=blog&aduco=exploring-the-atlantic-ocean-in-insights&adupt=lead_gen&sf_id=70139000001eKGfAAM).


## Licensing
Copyright 2019 Esri

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

