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

# Run commands.
CMD [ "exec", "\"@\"" ]
