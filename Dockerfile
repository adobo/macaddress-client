FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY macaddress-client.py ./
ENTRYPOINT [ "python", "./macaddress-client.py" ]
