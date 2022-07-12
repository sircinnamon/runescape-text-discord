FROM python:alpine
RUN apk add --update --no-cache gcc libc-dev git musl-dev linux-headers g++
RUN apk add --no-cache jpeg-dev zlib-dev freetype-dev
RUN MULTIDICT_NO_EXTENSIONS=1 YARL_NO_EXTENSIONS=1 pip install --no-cache-dir py-cord requests runescape-text Pillow
WORKDIR /runescape/
CMD python -u /runescape/runescapeBot.py
ADD *.py /runescape/