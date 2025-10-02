FROM ubuntu:25.04

# Set timezone
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Updating and Upgrading
RUN apt-get -y update
RUN apt-get -y upgrade

# Installs
RUN apt-get -y install nginx
RUN apt-get -y install php8.4 php8.4-cli php8.4-fpm
RUN apt-get -y install htop nano
RUN apt-get -y autoremove
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN pip install pip setuptools wheel --break-system-packages spacy
RUN pip install --break-system-packages spacy

# Copy config files into container
COPY config/default /etc/nginx/sites-available/default

# Copy api files into container
COPY webroot/ /var/www/html/
RUN chown -R www-data:www-data /var/www/html/
RUN chmod -R 755 /var/www/html/
RUN chmod +x -R /var/www/html/

# Copy ner app files into container
COPY ner_app/ /var/ner_app/
RUN chown -R www-data:www-data /var/ner_app/
RUN chmod -R 755 /var/ner_app/
RUN chmod +x -R /var/ner_app/


# Expose port
EXPOSE 8080/tcp

RUN python3 -m spacy validate
RUN python3 -V

# Start services and hang out
ENTRYPOINT service php8.4-fpm start && nginx -t && service nginx start && tail -f