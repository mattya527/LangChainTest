FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

USER root
RUN apt update && apt upgrade -y &&\
    apt install -y mecab mecab-ipadic-utf8 libmecab-dev wget \
    fonts-ipafont-gothic fontconfig \ 
    build-essential libbz2-dev libdb-dev \
    libreadline-dev libffi-dev libgdbm-dev liblzma-dev \
    libncursesw5-dev libsqlite3-dev libssl-dev \
    zlib1g-dev uuid-dev pandoc libmagic1  cmake  locales\
    && locale-gen ja_JP.UTF-8 \
    && update-locale LANG=ja_JP.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# ロケール環境変数の設定
ENV LANG=ja_JP.UTF-8
ENV LANGUAGE=ja_JP:ja
ENV LC_ALL=ja_JP.UTF-8
ENV PYTHON_VERSION=3.12.6

# fontの反映
RUN fc-cache -f -v 
RUN cp /etc/mecabrc /usr/local/etc/mecabrc
RUN echo 'root:password' | chpasswd
ARG USERNAME=synclab01
ARG GROUPNAME=synclab01
ARG UID=1000
ARG GID=1000
ARG WORKDIR=/home/$USERNAME/
ARG PROJECT_NAME=devaizu
RUN groupadd -g $GID $GROUPNAME && \
    useradd -m -s /bin/bash -u $UID -g $GID $USERNAME

WORKDIR ${WORKDIR}
COPY ${PROJECT_NAME}/src/requirements.txt ${WORKDIR}requirements.txt
RUN chown -R ${USERNAME}:${GROUPNAME} ${WORKDIR}requirements.txt

# Pythonのインストール
RUN wget -P /tmp https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && tar zxvf /tmp/Python-${PYTHON_VERSION}.tgz -C /tmp/ && \
    cd /tmp/Python-${PYTHON_VERSION} && ./configure && \
    make && make install

# 環境変数の追加
ENV PATH="/usr/local/python/bin:${PATH}"

# libreofficeのインストール
# COPY ${PROJECT_NAME}/LibreOffice_24.8.0_Linux_x86-64_deb.tar.gz /tmp/LibreOffice_24.8.0_Linux_x86-64_deb.tar.gz
# RUN tar xvfz /tmp/LibreOffice_24.8.0_Linux_x86-64_deb.tar.gz -C /tmp
# RUN dpkg -i /tmp/LibreOffice_24.8.0.3_Linux_x86-64_deb/DEBS/*.deb

USER $USERNAME

# 先にtorchをインストールしてからでないとflash-attnがインストールできない
# RUN pip3 install -r ${WORKDIR}requirements.txt
# RUN /usr/local/python/bin/pip3 install flash-attn==2.6.3
