#!/usr/bin/env make
#
# NOTE: Make target cannot be the name of a runtime argument, otherwise Makefile
# will go into an infinite loop.

.PHONY: version check setup run start

export APP_VERSION ?= $(shell git rev-parse --short HEAD)
export GIT_REPO_ROOT ?= $(shell git rev-parse --show-toplevel)

export DOCKER_IMAGE_NAME ?= pydistrict_pbt

export USER_ID = $(shell id -u $(whoami))
export GROUP_ID = $(shell id -u $(whoami))

version:
	@echo '{"Version": "$(APP_VERSION)"}'

# Start the development server.
#
# NOTE: Make sure to have your SSH credentials mounted in ~/.ssh.
check:
	@echo "Checking system dependencies..."
	# GNU Make 4.2.1
	# Built for x86_64-pc-linux-gnu
	# Copyright (C) 1988-2016 Free Software Foundation, Inc.
	# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
	# This is free software: you are free to change and redistribute it.
	# There is NO WARRANTY, to the extent permitted by law.
	@echo $$(make --version)
	# Docker version 19.03.8, build afacb8b7f0
	@echo $$(docker --version)
	# git version 2.27.0
	@echo $$(git --version)

docker-build:
	docker build \
		--file $(GIT_REPO_ROOT)/Dockerfile \
		--tag $(DOCKER_IMAGE_NAME):$(APP_VERSION) \
		.

# From: https://stackoverflow.com/a/14061796
# If the first argument is "run"...
ifeq (docker-run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

# Lifts command into `docker run` context.
#
# See this blog post for Dockerizing a React.js application:
# https://mherman.org/blog/dockerizing-a-react-app/#docker
docker-run: docker-build
	docker run \
		--rm \
		-it \
		-v $(shell pwd):/app \
		--net=host \
		-u $(USER_ID):$(GROUP_ID) \
		$(DOCKER_IMAGE_NAME):$(APP_VERSION) \
		bash -c "$(RUN_ARGS)"

docker-bash:
	$(MAKE) docker-run bash

# Update dependencies.
#
# In order to use the generated 'requirements.txt' file, make sure to reboot the
# Docker container. Otherwise, 'requirements.txt' will be overwritten.
update-deps:
	# `cd` into ${WORKDIR}/src in order to install Python dependencies with
	# proper context both inside and outside Docker container. Otherwise, will
	# show 'via -r /app/src/requirements.txt' instead of just 'via -r
	# requirements.txt'.
	#
	# Need to use `bash -c` because otherwise `docker run` will strip context of
	# `cd` and leave it interpreted as an executable.
	#
	# `--allow-unsafe` for `pip` and `setuptools` alone should be fine. See this
	# Stack Overflow answer: https://stackoverflow.com/a/58864335
	$(MAKE) docker-run "cd /app && /usr/local/bin/pip-compile --generate-hashes --allow-unsafe --output-file=requirements.txt requirements.in"

docker-pyre:
	$(DOCKER) docker-run "pyre"
