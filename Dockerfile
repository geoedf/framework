FROM ubuntu:18.04

# System packages
RUN apt-get update && \
    apt-get -y install python3.6 \
                       python3-pip \
                       python3-setuptools \
                       python3-wheel \
                       libpython3-dev \
		       wget \
		       curl \
		       gcc \
		       g++ \
		       openssh-client

RUN python3 -m pip install -U pip setuptools

RUN pip3 install geoedfframework==0.6.0

# Install miniconda to /opt/conda
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

RUN bash Miniconda3-latest-Linux-x86_64.sh -p /opt/conda -b

RUN rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH=/opt/conda/bin:${PATH}

RUN conda update -y conda

RUN conda create -n geoedf python=3.6

RUN conda install -n geoedf -c conda-forge -y qgis

ENV PATH=/usr/local/bin:$PATH

ENV PYTHONPATH=/usr/local/lib/python3.6/dist-packages:$PYTHONPATH

RUN chmod a+x /usr/local/bin/*.sh && \
    chmod a+x /usr/local/bin/*.py && \
    chmod -R go+rX /usr/local/lib/python3.6/dist-packages
