FROM debian:bullseye

# install docker cli
RUN apt-get update \
    && apt-get install -y \
       ca-certificates \
       curl \
       gnupg \
       lsb-release \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
        $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && apt-get install -y kubectl \
    && apt-get install -y python3 python3-pip \
    && apt-get install -y vim

WORKDIR /work

COPY install-kind.sh entrypoint.sh /work

RUN chmod 755 ./install-kind.sh ./entrypoint.sh \
    && ./install-kind.sh

CMD ["/work/entrypoint.sh"]