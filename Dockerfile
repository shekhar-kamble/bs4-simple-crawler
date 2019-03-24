FROM python:2.7.14-stretch

MAINTAINER Shekhar Kamble <shekhar.ak0@gmail.com>

##############################################################################
# OS Updates and Python packages
##############################################################################

RUN apt-get update && \
    apt-get install -y apt-transport-https

# Install Supervisor with dependencies
RUN apt-get update && \
    apt-get install -y supervisor && \
    rm -rf /var/lib/apt/lists/*


##############################################################################
# Configure application
##############################################################################

WORKDIR /var/app

RUN pip install virtualenv
RUN virtualenv /var/app
RUN /var/app/bin/pip install setuptools --upgrade

##############################################################################
# Configure supervisord
##############################################################################

RUN useradd supervisor -s /bin/false
RUN mkdir -p /var/log/supervisord
RUN chown -R supervisor:supervisor /var/log/supervisord

##############################################################################
# Copy app and install requirements
##############################################################################
COPY requirements.txt /var/app/requirements.txt
RUN  /var/app/bin/pip install -r /var/app/requirements.txt
ADD . /var/app

##############################################################################
# Run start.sh script when the container starts.
# Note: If you run migrations etc outside CMD, envs won't be available!
##############################################################################
ENTRYPOINT ["/var/app/deploy/run-server.sh"]

EXPOSE 8080