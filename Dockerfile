FROM python:3.6-jessie
RUN pip install --no-cache-dir discord requests runescape-text Pillow
ADD *.py /runescape/
WORKDIR /runescape/
CMD python /runescape/runescapeBot.py
