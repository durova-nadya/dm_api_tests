FROM python:latest

COPY . .
RUN pip3 install -r requiments.txt

CMD ["pytest", "/tests"]