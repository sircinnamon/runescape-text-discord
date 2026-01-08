FROM python:3.13-alpine
RUN apk add --update --no-cache gcc libc-dev git musl-dev linux-headers g++
RUN apk add --no-cache jpeg-dev zlib-dev python3-dev freetype-dev
RUN MULTIDICT_NO_EXTENSIONS=1 YARL_NO_EXTENSIONS=1 pip install --no-cache-dir requests runescape-text Pillow
RUN pip install --no-cache-dir "py-cord>=2.7"
WORKDIR /runescape/
CMD python -u /runescape/runescapeBot.py
ADD *.py /runescape/