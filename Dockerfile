FROM --platform=linux/amd64 python:3.11
# FROM --platform=$BUILDPLATFORM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t eastor112/solartherm-backend:mises --push .
