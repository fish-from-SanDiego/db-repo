ARG PY_IMAGE_TAG
FROM python:$PY_IMAGE_TAG

WORKDIR /usr/src/explain

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "explain.py" ]
