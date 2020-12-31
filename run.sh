#!/bin/bash

if [ ! -d "logs" ]; then
	mkdir "logs"
fi

if [ ! -e ".keyfile" ]; then
	echo "Keyfile missing: '.keyfile'"
	exit 1
fi

docker stop runescape
docker rm runescape
docker run \
	-d \
	--name runescape \
	-v $(pwd)/logs:/runescape/logs \
	-v $(pwd)/.keyfile:/runescape/.keyfile \
	-v /etc/localtime:/etc/localtime:ro \
	runescapebot:latest
