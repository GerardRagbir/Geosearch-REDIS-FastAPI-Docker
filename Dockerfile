FROM python:3.10-alpine
LABEL MAINTAINER="Gerard Ragbir"
WORKDIR /geosearch/
RUN pip install requirements.txt
ADD main.py .
CMD ["python", "./main.py"]
HEALTHCHECK NONE