# jupyter image w/ Python
FROM jupyter/scipy-notebook

LABEL maintainer="Insights"

USER root

# uncomment to set working directory in container
# WORKDIR /data

# uncomment to copy certificate and key for tls (https)
# COPY /certs/* /etc/ssl/certs/

# uncomment to copy data to the container
# COPY /data/* /data/

# R pre-requisites
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata \
    gfortran \
    gcc && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $NB_UID

# R packages including IRKernel which gets installed globally.
RUN conda install --quiet --yes \
    'rpy2=2.8*' \
    'r-base=3.4.1' \
    'r-irkernel=0.8*' \
    'r-plyr=1.8*' \
    'r-jsonlite=1.5*' \
    'r-data.table=1.11.4*' \
    'r-devtools=1.13*' \
    'r-tidyverse=1.1*' \
    'r-shiny=1.0*' \
    'r-rmarkdown=1.8*' \
    'r-forecast=8.2*' \
    'r-rsqlite=2.0*' \
    'r-reshape2=1.4*' \
    'r-nycflights13=0.2*' \
    'r-caret=6.0*' \
    'r-rcurl=1.95*' \
    'r-crayon=1.3*' \
    'r-randomforest=4.6*' \
    'r-htmltools=0.3*' \
    'r-sparklyr=0.7*' \
    'r-htmlwidgets=1.0*' \
    'r-hexbin=1.27*' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# install the kernel gateway, arcgis Python API, and geopandas
RUN pip install --quiet jupyter_kernel_gateway==2.1.0 arcgis geopandas

# environment settings for kernel gateway
ENV KG_ALLOW_ORIGIN='*'
ENV KG_LIST_KERNELS='True'

# run kernel gateway on container start, not notebook server
EXPOSE 9999

# set tls (https) on the kernel gateway
CMD ["jupyter", "kernelgateway", "--KernelGatewayApp.ip=0.0.0.0", "--KernelGatewayApp.port=9999", "--KernelGatewayApp.allow_credentials='*'", "--KernelGatewayApp.allow_headers='*'", "--KernelGatewayApp.allow_methods='*'", "--KernelGatewayApp.certfile=/etc/ssl/certs/<your_cert.crt>", "--KernelGatewayApp.keyfile=/etc/ssl/certs/<your_key>.key"]
