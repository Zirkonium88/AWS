#!/bin/bash

# Build the container
docker build -t rlayerbuilder .

# Run the container
docker run -it \
    --name rlayerbuilder \
    -v ${pwd}:/opt/R/ \
    -e R_VERSION="3.6.1" \
    rlayerbuilder /bin/bash

docker cp rlayerbuilder:/opt/R/ .

docker rm rlayerbuilder