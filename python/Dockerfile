FROM php:7.1-apache
LABEL maintainer="Juan Ramón Riveiro"

# Enable Apache Rewrite Module
RUN a2enmod rewrite


VOLUME /root

# Copy init scripts and custom .htaccess
COPY docker-entrypoint.sh /entrypoint.sh
COPY makedb.php /makedb.php

ENTRYPOINT ["/entrypoint.sh"]
CMD ["apache2-foreground"]
