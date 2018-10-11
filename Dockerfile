FROM ubuntu:16.04
# MAINTAINER kensuke-mi <kensuke.mit@gmail.com>

# python3.6
COPY apt.conf /etc/apt/apt.conf
RUN apt-get update
RUN apt-get install -y software-properties-common
# RUN apt-get install -y vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
# RUN apt-get install -y git

RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

# ソフトウェアのダウンロード元
ENV CRFSUITE_SOURCE_URL https://github.com/downloads/chokkan/crfsuite/crfsuite-0.12.tar.gz
ENV LIB_LBFGS_SOURCE_URL https://github.com/downloads/chokkan/liblbfgs/liblbfgs-1.10.tar.gz
ENV KYOTOCABINET_SOURCE_URL http://fallabs.com/kyotocabinet/pkg/kyotocabinet-1.2.76.tar.gz

## apt-getで依存ライブラリのインストール
RUN apt-get update && \
apt-get install -y software-properties-common --fix-missing && \
apt-get update

### gccのインストール
RUN apt-get install -y gcc --fix-missing
RUN apt-get install -y g++ --fix-missing
RUN apt-get install -y swig2.0 --fix-missing
RUN apt-get install -y make --fix-missing

### DB郡とその他utilsのインストール
RUN apt-get install -y \
libz-dev \
zlib1g-dev \
libssl-dev \
libreadline-dev \
build-essential \
libpq-dev \
vim \
wget \
curl \
git \
openssh-server \
unzip \
fonts-ipafont-gothic \
fonts-ipafont-mincho \
--fix-missing

### Rubyのインストール
RUN apt-add-repository ppa:brightbox/ruby-ng
RUN apt-get update
RUN apt-get -y install ruby2.4 ruby-dev ruby2.4-dev

### 日本語フォント群のインストール
RUN apt-get install -y fonts-vlgothic fonts-horai-umefont fonts-umeplus
### mecabの辞書を先にutf-8でインストールしておく
RUN apt-get install -y mecab mecab-ipadic-utf8
RUN apt-get install -y mecab libmecab-dev
RUN apt-get -y install pandoc
### apt-getでインストールすると、標準（と期待されている）の辞書パスと違う辞書パスになる。だからシンボリックリンクを作成
RUN ln -s /var/lib/mecab/dic/ /usr/lib/mecab/dic
RUN ln -s /usr/bin/mecab-config /usr/local/bin/mecab-config

# libLBFGS
WORKDIR /opt
RUN wget -c ${LIB_LBFGS_SOURCE_URL}
RUN tar xzvf liblbfgs-1.10.tar.gz
RUN cd liblbfgs-1.10 && ./configure && make && make install

# CRFsuite
WORKDIR /opt
RUN wget -c ${CRFSUITE_SOURCE_URL}
RUN tar xzvf crfsuite-0.12.tar.gz
RUN cd crfsuite-0.12 && ./configure && make && make install

# KyotoCabinet
WORKDIR /opt
RUN wget -c ${KYOTOCABINET_SOURCE_URL}
RUN tar zxvf kyotocabinet-1.2.76.tar.gz
WORKDIR /opt/kyotocabinet-1.2.76
RUN ./configure && make && make install

# ruby用のライブラリインストール
WORKDIR /opt
RUN gem install oj nokogiri mecab moji levenshtein
RUN git clone https://github.com/abicky/crfsuite.git
WORKDIR /opt/crfsuite/swig/ruby/
RUN ./prepare.sh --swig && ruby extconf.rb && make install

WORKDIR /opt
RUN wget http://fallabs.com/kyotocabinet/rubypkg/kyotocabinet-ruby-1.32.tar.gz
RUN tar xvzf kyotocabinet-ruby-1.32.tar.gz
WORKDIR /opt/kyotocabinet-ruby-1.32
RUN sed -i 's/Config/RbConfig/g' extconf.rb
RUN sed -i 's/define _KC_YARV_//g' kyotocabinet.cc
RUN ruby extconf.rb && make install

RUN ldconfig

# jawikify
# WORKDIR /opt    # by mazda
ENV JAWIKIFY_WORK_DIR /opt/jawikify
RUN mkdir -p ${JAWIKIFY_WORK_DIR}
WORKDIR ${JAWIKIFY_WORK_DIR}
# モデル・インベントリのデータをダウンロードします。（合計、およそ2GB程度）
COPY ./download_data.sh .
RUN ./download_data.sh
ADD . ${JAWIKIFY_WORK_DIR}

# 日本語環境に切り替え
RUN apt-get install -y language-pack-ja-base language-pack-ja
ENV LANG=ja_JP.UTF-8

# pip install
COPY requirements.txt ${WORKDIR}/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# サーバの立ち上げ
EXPOSE 8079

CMD bash -c "source ./setup.sh; python3.6 run_server.py -p 8079"
# CMD ["/bin/bash", "-c", "tail -f /dev/null"]
