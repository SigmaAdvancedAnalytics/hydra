FROM debian:jessie-slim
MAINTAINER Joshua Barber "j.barber501@gmail.com"

USER root

# Install basic system packages and add /bin/bash as default shell
RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
        openssh-server \
        build-essential \
        apt-utils \
        curl \
        wget \
        git \
        bzip2 \
        ca-certificates \
        sudo && \
    rm /bin/sh && ln -s /bin/bash /bin/sh

# Configure and install Yarn and NodeJS 8
RUN curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash - && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && apt-get install -yq --no-install-recommends \ 
        apt-transport-https \
        nodejs \
        yarn

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.10.0/tini && \
    echo "1361527f39190a7338a0b434bd8c88ff7233ce7b9a4876f3315c22fce7eca1b0 *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

# Set environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /home

# Franchise setup
RUN git clone --depth 1 https://github.com/HVF/franchise.git && \  
    cd franchise && \
    yarn install

WORKDIR /home/franchise 

# Configure container startup
ENTRYPOINT ["/usr/local/bin/tini", "--"]
#CMD ["npx","franchise-client@0.2.3"]
CMD ["/bin/bash","npx franchise-client@0.2.3 & yarn start"]

EXPOSE 3000