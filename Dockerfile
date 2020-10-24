FROM python:3.8.0
LABEL maintainer="Ying Wang"
LABEL application="pydistrict_pbt"

# Set environment variables.
ENV DEBIAN_FRONTEND=noninteractive
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
ENV PYTHONDONTWRITEBYTECODE=1

# Get package lists, important for getting 'curl' and such.
RUN apt-get -y update

# Install build dependencies.
RUN apt-get install -y apt-utils
RUN apt-get install -y curl

# Setup workdirectory.
RUN mkdir /app
WORKDIR /app

# Install `pip-tools` in order to initially scaffold 'requirements.txt' if it
# does not already exist.
RUN pip3 install pip-tools

# Install requirements.txt.
COPY requirements.txt ${WORKDIR}/requirements.txt
RUN pip3 install -r ${WORKDIR}/requirements.txt

# Install Watchman (for running 'pyre incremental'):
# https://facebook.github.io/watchman/docs/install.html
RUN curl -Ls -o /tmp/watchman.zip https://github.com/facebook/watchman/releases/download/v2020.09.21.00/watchman-v2020.09.21.00-linux.zip
RUN unzip /tmp/watchman.zip -d /tmp
RUN mkdir -p /usr/local/var/run/watchman
RUN cp /tmp/watchman-v2020.09.21.00-linux/bin/* /usr/local/bin
RUN cp /tmp/watchman-v2020.09.21.00-linux/lib/* /usr/local/lib
RUN chmod 755 /usr/local/bin/watchman
RUN chmod 2777 /usr/local/var/run/watchman

# Run commands.
CMD [ "exec", "\"@\"" ]
