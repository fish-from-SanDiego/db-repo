ARG PY_IMAGE_TAG
FROM python:$PY_IMAGE_TAG

WORKDIR /usr/src/db_setup

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "bash", "-c", "./scripts/run_py_scripts.sh" ]