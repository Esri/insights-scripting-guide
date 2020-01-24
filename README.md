# Insights Scripting Guide

This guide offers a reference for creating custom features in ArcGIS Insights using Python and R.  From deploying a Kernel Gateway to using the script editor to visualize data, use this resource as the definitive guide for Insights scripting topics.
 

## Prerequisites

* ArcGIS Insights (version 2020.x)
* Anaconda (version 3.7)

Scripting is not available in ArcGIS Online versions of Insights._ 

## Python and R Dependencies

* See needed Python and R [dependencies](gateway/insights-base.yml) 


## Kernel Gateway Setup 

Insights supports connections to Jupyter's Kernel Gateway version 2.1.0.  Jupyter's Kernel Gateway is an open source web server which is distributed through ```conda-forge``` and other channels. To learn how to setup a Kernel Gateway with the needed dependencies choose one of the following deployment sections. 

* [How to deploy a Kernel Gateway with dependencies using Anaconda](#How-to-deploy-a-Kernel-Gateway-with-dependencies-using-Anaconda)
* [How to deploy a Kernel Gateway with dependencies using Docker](#How-to-deploy-a-Kernel-Gateway-with-dependencies-using-Docker)
   

### How to deploy a Kernel Gateway with dependencies using Anaconda

It's reccomended to read the section on Planning a Scipting Environment before following these steps.

1) Install [Anaconda v3.7](https://www.anaconda.com/distribution/#download-section)
2) Create a folder named ```gateway```
3) Copy ```selfsign.py``` and ```insights-base.yml``` into your ```gateway``` folder
4) Open _Anaconda's command promt_ and CD into the ```gateway``` folder
5) Run the following commands

    ```
    conda env create -f insights-base.yml
    conda activate insights-base
    python selfsign.py
    ```

6) Start the Kernel Gateway by running this command:

    ```
    jupyter kernelgateway --KernelGatewayApp.ip=0.0.0.0 --KernelGatewayApp.port=9999 --KernelGatewayApp.allow_origin='*'
     --KernelGatewayApp.allow_credentials='*' --KernelGatewayApp.allow_headers='*' --KernelGatewayApp.allow_methods='*'
      --JupyterWebsocketPersonality.list_kernels=True --certfile=./server.crt --keyfile=./server.key
    ```
_Note: Make sure the start command is single line (not 3 lines)_

To stop a Kernel Gateway:

Press _Control-C_ in the window running the Kernel Gateway. Alternatively, close the window.


### How to deploy a Kernel Gateway with dependencies using Docker

...Coming soon...


## Planning a Scipting Environment

A variety of options exist for hosting a Kernel Gateway.  A Kernel Gateway can be installed on the same machine as ArcGIS Insights or on a different machine.  

Typically, installing the Kernel Gateway on the same machine as Insights is the easiest approach (especially if you using Insights Desktop).  In the case of an ArcGIS Enterprise installation of Insights, more consideration is needed.  For the enterpise case, the machine running Insights in the web browser and the machine(s) running Insights Service all need to communicate with the Kernel Gateway.

Kernel Gateway URL address referencing is also important.   Consider these urls pointing to a fake machine named pickle, on a fake domain named esri.com  :

1) http://localhost:9999
2) https://localhost:9999
3) http://pickle:9999
4) https://pickle:9999
5) http://12.120.95.153:9999 
6) https://12.120.95.153:9999
7) http://pickle.esri.com:9999
8) https://pickle.esri.com:9999

Of these addresses only 6 and 8 are ideal for ensuring communication between ArcGIS Insights and a Kernel Gateway. Over a network, these two address stand the best chance because item 6 (the IP address) uniquely represents the machine with the Kernel Gateway and item 8 (the FQDN address) includes both the machine name and domain name which together form a unique address, which Insights uses to resolve the Kernel Gateway on the network.

_Pro Tip_ : Insights Desktop is a little more flexible.  If you install the Kernel Gateway on the same machine as Insights Desktop, it's possible to create a connection using item 1, 3, 5, and 7.

For further reading choose a subsection most relavant and the section on troubleshooting, if you are having problems connecting to your Kernel Gateway environment:

### _Insights Desktop with Kernel Gateway:_

Either install Jupyter's Kernel Gateway on the same machine as Insights Desktop (easyiest) or put the Kernel Gateway on a different machine and ensure both machines can communicate with each other via the office, home or cloud network.  Choose a URL reference similar to items 1, 3, 5, and 7 when creating a connection within Insights to the Kernel Gateway.

### _Insights for ArcGIS Enterprise:_  

Install Jupyter's Kernel Gateway on machine that is accessible by ArcGIS Enterprise and the machine which will access Insights via the web browser. Choose a URL reference similar to items 6 and 8 when creating a connection within Insights to the Kernel Gateway.

### _Insights for ArcGIS Enterprise running the Cloud:_ 

In a case where you have ArcGIS Enterprise and Insights running in the Cloud and would like to enable scripting, this requires advanced networking skills to ensure Insights can communicate with the Kernel Gateway.  The machine(s) hosting Insights Service in the cloud need to be able to access the Kernel Gateway and so does the machine running Insights in the web browser. To achieve this landscape, typically a Kernel Gateway will be installed in the cloud.  While it may be possible to locate the Kernel Gateway on an office network, a static IP would need to be assigned to the Kernel Gateway and firewall settings should be updated to protect against abuse.

Whether a in the cloud or on-premise, for security reasons it is important to ensure that all IP address trying to reach the Kernel Gateway are blocked except those from Insights Service machines and clients running Insights in the web browser.  Amazon offers blocking and IP  filtering via it's Security Groups feature.  In Azure, you can filter network traffic  using a Network Security Group.  If planning a Kernel Gateway, on-premise with ArcGIS Enterprise hosted in the cloud, consult the person or team responsible for managing you're computer ifrastructure and network.


### _Hybrid: On-premises Insights and Kernel Gateway running the Cloud:_

This requires advanced networking skills to ensure Insights can communicate with the Kernel Gateway.  The machine(s) hosting Insights Service on-premsis and the machine running Insights in the web browser need to be able to access the Kernel Gateway. When running a Kernel Gateway in the cloud, for security reasons it is important to ensure that all IP address trying to reach the Kernel Gateway are blocked except those from Insights Service machines and clients running Insights in the web browser.  Amazon offers blocking and IP  filtering via it's Security Groups feature.  In Azure, you can filter network traffic  using a Network Security Group.  

## Troubleshooting 

_Insights is running in the web browser and when connecting to a Kernel Gateway an error says "Not able to add this connection. Try with a different URL or web socket or check if your gateway is running."_

If you've followed the guide (and ran the selfsign.py file), you have created a self signed SSL certificate. It may be possible that Insights cannot make a connection because the web browser itself does not trust the certificate. To work around this problem open the kernel gateway URL in the web browser and accept the browser warning. Then try connecting again.



_My Kernel Gateway is on a different machine and I am having trouble making a connection using Insights?_

A fundemental way to toubleshoot this problem is first confirm that the computer(s) running Insights can talk to the Kernel Gateway computer. Try getting the IP address of the machine running your Kernel Gateway and then use the ```ping``` command to see if the ping message was received. 

Using windows, run ```ipconfig``` and reference the Iv4 address.  Using mac, run ```ipconfig getifaddr en0``` and note the address.  Next from the machine(s) running Insights (Insights Desktop or Insights Service machines plus the machine running Insights in the web browser) run ```ping your-kernel-gateway-ip-address```.  If you get a reply, that means Insights should be able to make a connection.


## Contribute

If you wish to contribute or have questions, please create an issue or pull request.