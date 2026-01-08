#!/bin/bash

if [ ! -d "logs" ]; then
	mkdir "logs"
fi

if [ ! -e ".keyfile" ]; then
	echo "Keyfile missing: '.keyfile'"
	exit 1
fi

docker stop runescape-dev
docker rm runescape-dev
docker run \
	-d \
	--name runescape-dev \
	-v $(pwd)/logs:/runescape/logs \
	-v $(pwd)/.keyfile:/runescape/.keyfile \
	-v /etc/localtime:/etc/localtime:ro \
	runescapebot:dev
