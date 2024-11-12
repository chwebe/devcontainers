FROM python:alpine AS compile-image

RUN apk update && \ 
    apk add --no-cache gcc bash musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:alpine AS build-image
COPY --from=compile-image /root/.local /root/.local

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]
