FROM php:7.3-apache

LABEL maintainer="Juan Ramón  juanriveiro@gmail.com"
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

# Instalarmos Composer: 
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Por último instalamos node.js
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
RUN apt-get -y install nodejs

RUN a2enmod rewrite

EXPOSE 80
CMD apachectl -D FOREGROUND

WORKDIR /var/www/html/