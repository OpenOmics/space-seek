# Base image for spaceranger,
# uses Ubuntu Noble
FROM ubuntu:24.04

############### ABOUT ###############
# Depedencies of spaceranger:
# • https://www.10xgenomics.com/support/software/space-ranger/downloads/space-ranger-system-requirements
# • https://www.10xgenomics.com/support/software/space-ranger/downloads/space-ranger-installation
# @TLDR: 
#   • Ubuntu >= 14.04
#   • AVX capable CPU, >= 8 cores, >= 32GB RAM
#   • spaceranger mkfastq requires bcl2fastq2 (v2.20 or later),
#     this is NOT install in this dockerfile since we do not
#     need to run spaceranger mkfastq.
#      •  https://emea.support.illumina.com/downloads/bcl2fastq-conversion-software-v2-20.html   
LABEL maintainer=kuhnsa@nih.gov

############### ARGS ################
# Spaceranger download URL, see README.md for more info,
# the URL will look like and it can be found as part
# of the download curl/wget commands:
# https://cf.10xgenomics.com/releases/spatial-exp/spaceranger-4.0.1.tar.gz?Expires=123&Key-Pair-Id=ABC&Signature=1a2b3c4d..."
ARG SPACERANGER_URL="https://cf.10xgenomics.com/releases/spatial-exp/spaceranger-4.0.1.tar.gz?Expires=1756455545&Key-Pair-Id=APKAI7S6A5RYOXBWRPDA&Signature=VK-8EdygyebsdswVRsGj~z1KQ~ox0oucaSNd1VDp7XdYR9MVCsWLYHwlKSvmjRvakAWxPPVSc66TNOYx98zdtzLj~-XK6HliO6IeUW5Jlugv7b0i8dayLb~7F1Ouxfu3~FLqu01wvi1f4qoCFBkNTtLmL0IC-Yptk6ZnC-qQ6WHjenyX3NShmy9bIAWOtbmT2udEl6ExUa0WqChieIjYvjrdcLf5D5boy-D5DluxDAWEzoA8ufTNABIiyuylPxLeZkdlLNTyspm0zXA0Qhpe~qW92O-cRiKnR2jPi0YgR2oHxhfQY~p5K91LErPoKPQa4L961YUzU-TamKYiLDCK0Q__" 

############### INIT ################
# Create Container filesystem specific 
# working directory and opt directories
# to avoid collisions with the host's
# filesystem, i.e. /opt and /data
RUN mkdir -p /opt2 && mkdir -p /data2
WORKDIR /opt2 

# Set time zone to US east coast 
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
        && echo $TZ > /etc/timezone

############### SETUP ################
# This section installs system packages 
# required for your project. If you need 
# extra system packages add them here.
RUN apt-get update \
    && apt-get -y upgrade \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        build-essential \
        bzip2 \
        ca-certificates \
        curl \
        gawk \
        git \
        gzip \
        locales \
        # python/3.12.3
        python3 \
        python3-pip \
        python3-pandas \
        python3-numpy \
        python3-scipy \
        # R/4.3.3
        r-base \
        # seurat/5.0.1
        r-cran-seurat \
        unzip \
        wget \
        zlib1g-dev \
    && apt-get clean && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the locale
RUN localedef -i en_US -f UTF-8 en_US.UTF-8

# Make python3 the default interpreter
# and install Python Packages 
RUN ln -sf /usr/bin/python3 /usr/bin/python

############### INSTALL ################
# Install spaceranger 4.0.1, requires a
# 10xgenomics account to download, and
# the download URL, which can be found
# on the downloads page:
# https://www.10xgenomics.com/support/software/space-ranger/downloads 
RUN curl -o /opt2/spaceranger-4.0.1.tar.gz "${SPACERANGER_URL}" \
        && tar -xvf /opt2/spaceranger-4.0.1.tar.gz -C /opt2/ \
        && rm /opt2/spaceranger-4.0.1.tar.gz 

# Install GNU which, increases compatability
# with which distros included with Debian/Rocky
# linux installations, this version of which
# includes extra options that the ubuntu version 
# does not have. The gnu verison is backwards 
# compatiable with the ubunutu version.
RUN wget --no-check-certificate -O /opt2/which.tar.gz https://ftp.gnu.org/gnu/which/which-2.21.tar.gz \
        && tar -xvf /opt2/which.tar.gz -C /opt2/ \
        && rm /opt2/which.tar.gz \
        && cd /opt2/which-2.21/ \
        && ./configure --prefix=/opt2/which-2.21 \
        && make \
        && make install
WORKDIR /opt2

################ POST #################
# Add Dockerfile and export important 
# environment variables
ADD Dockerfile /opt2/spaceranger_4-0-1.dockerfile
RUN chmod -R a+rX /opt2
ENV PATH="/opt2/which-2.21/bin:/opt2/spaceranger-4.0.1:${PATH}"
WORKDIR /data2
