FROM amazonlinux:2

# Install presequities
RUN yum update -y \
    && yum install -y \
    sudo \
    wget \
    readline-devel \
    libX11-devel \
    libXt-devel \
    curl-devel \
    gcc-c++ \
    gcc-gfortran \
    zlib-devel \
    openssl-devel \
    libxml2-devel \
    yum-utils \
    tar \
    bzip2-devel \
    make \
    which \
    java-1.8.0-openjdk-devel \
    perl perl-Data-Dumper \
    epel-release

# workaround for making R build work
# issue seems similar to https://stackoverflow.com/questions/40639138/configure-error-installing-r-3-3-2-on-ubuntu-checking-whether-bzip2-support-suf
RUN yum install -y \
    R \
    zip

# RUN sudo yum-builddep R
RUN set -euo pipefail &&\
    mkdir -p /opt/R/ &&\
    chown $(whoami) /opt/R/

# Change your R Versione accordingly
RUN wget https://cran.uni-muenster.de/src/base/R-3/R-3.6.1.tar.gz &&\
    tar -xf R-3.6.1.tar.gz &&\
    mv R-3.6.1/* /opt/R/

RUN cd /opt/R/ &&\
    ./configure --prefix=/opt/R/ --exec-prefix=/opt/R/ --with-libpth-prefix=/opt/ --without-recommended-packages &&\
    make

# Install R packages
# We need JSON lite, add further R packages, if you want to --> install.packages(c("jsonlite"))
RUN /opt/R/bin/Rscript -e 'chooseCRANmirror(graphics=FALSE, ind=34); install.packages("jsonlite")'
ADD installDependencies.R /opt/R/bin/
RUN /opt/R/bin/Rscript /opt/R/bin/installDependencies.R

# Zip R binaries
RUN zip -r -q R.zip bin/ lib/ lib64/ etc/ library/ doc/ modules/ share/

CMD []
