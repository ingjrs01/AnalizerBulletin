FROM php:7.2-apache

LABEL maintainer="Mads Mønster @storebuddy.dk"
LABEL version="1.0"

RUN apt-get update && apt-get install -y \
    cron \
    anacron \
    git \
    libpcre3-dev \
    libmcrypt-dev \
    libxml2-dev \
    zlib1g-dev \
    libssh2-1 \
    libssh2-1-dev \
    libpng-dev \
    --no-install-recommends \
    && docker-php-ext-install -j$(nproc) pdo_mysql mbstring soap zip gd \
    && cp /usr/local/bin/php /usr/bin/

# Install PECL extensions
RUN pecl install xdebug && pecl install mcrypt-1.0.1 && pecl install ssh2-1.1.2
RUN docker-php-ext-enable xdebug mcrypt ssh2

# Install Phalcon
WORKDIR /usr/local/src
RUN git clone https://github.com/phalcon/cphalcon.git --branch v3.3.1 --single-branch
WORKDIR /usr/local/src/cphalcon/build
RUN ./install

WORKDIR /etc/php7/mods-available
RUN echo 'extension=phalcon.so' >> phalcon.ini
RUN docker-php-ext-enable phalcon

WORKDIR /var/www/