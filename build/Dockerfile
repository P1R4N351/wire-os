FROM debian:bookworm-20250630-slim

ARG UID
ARG GID
ARG USER_NAME
ARG DIR_PATH

RUN apt-get update && \ 
    apt-get install -y sudo build-essential chrpath cpio debianutils \
    diffstat expect file gcc git iputils-ping libacl1 liblz4-tool \
    locales python3 python3-git python3-jinja2 python3-pexpect \
    python3-subunit socat texinfo unzip wget xz-utils zstd git-core \
    gnupg flex bison gperf build-essential zip curl zlib1g-dev \
    libncurses5-dev x11proto-core-dev libx11-dev libz-dev \
    libxml-simple-perl libc6-dev libgl1-mesa-dev tofrodos libxml2-utils \
    xsltproc genisoimage gawk chrpath texinfo p7zip-full \
    android-sdk-libsparse-utils mime-support ruby subversion libssl-dev \
    protobuf-compiler pkg-config nano libtinfo5 ninja-build clang ccache \
    libc++-dev rsync cmake automake libtool patch

RUN ln -sf /bin/bash /bin/sh
RUN useradd -ms /bin/bash ${USER_NAME} && echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8
RUN usermod -u ${UID} ${USER_NAME} && groupmod -g ${GID} ${USER_NAME}

COPY patches/0001-runtime-arm-time64-go1.26.11.patch /tmp/go-arm-time64.patch

RUN set -e; \
    arch="$(dpkg --print-architecture)"; \
    for url in \
        "https://github.com/upx/upx/releases/download/v5.0.0/upx-5.0.0-${arch}_linux.tar.xz" \
        "https://go.dev/dl/go1.26.11.linux-${arch}.tar.gz" \
        "https://go.dev/dl/go1.26.11.src.tar.gz"; \
    do \
        wget -q "$url"; \
    done && \
    tar -xf upx-5.0.0-${arch}_linux.tar.xz && \
    mv upx-5.0.0-${arch}_linux/upx /usr/bin/ && \
    mkdir -p /tmp/go-boot && \
    tar -C /tmp/go-boot --strip-components=1 -zxf go1.26.11.linux-${arch}.tar.gz && \
    tar -C /usr/local -zxf go1.26.11.src.tar.gz && \
    patch -d /usr/local/go -p1 < /tmp/go-arm-time64.patch && \
    (cd /usr/local/go/src && GOROOT_BOOTSTRAP=/tmp/go-boot ./make.bash) && \
    touch /usr/local/go/.vicos-arm-time64-patched && \
    rm -rf /tmp/go-boot /tmp/go-arm-time64.patch upx-5.0.0-${arch}_linux *.deb *.tar.gz *.tar.xz

RUN ln -sf /usr/local/go/bin/go /usr/bin/go
ENV GO_EXE=/usr/local/go/bin/go
RUN mkdir -p /root/go

RUN wget https://github.com/ccache/ccache/releases/download/v4.11.3/ccache-4.11.3-linux-x86_64.tar.xz
RUN tar -xf ccache-4.11.3-linux-x86_64.tar.xz
RUN mv ccache-4.11.3-linux-x86_64/ccache /usr/bin/
RUN chmod +x /usr/bin/ccache

RUN chmod 0755 /usr/bin/upx

RUN ln -sf /usr/bin/python3 /usr/bin/python
RUN chmod 0755 /usr/local/bin
RUN ln -sf /usr/bin/ninja /usr/local/bin/ninja

USER ${USER_NAME}
WORKDIR ${DIR_PATH}
CMD ["/bin/bash"]
