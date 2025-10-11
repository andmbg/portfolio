#!/bin/bash
cp /etc/letsencrypt/live/somethingsomethingdata.eu/fullchain.pem /opt/portfolio/ssl-certs/
cp /etc/letsencrypt/live/somethingsomethingdata.eu/privkey.pem /opt/portfolio/ssl-certs/
chmod 644 /opt/portfolio/ssl-certs/fullchain.pem
chmod 600 /opt/portfolio/ssl-certs/privkey.pem

docker-compose -f /opt/portfolio/docker-compose.prod.yml restart nginx

