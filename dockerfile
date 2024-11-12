FROM python:alpine

RUN apk add --no-cache gcc bash musl-dev libffi-dev
RUN pip install --no-cache-dir python-binance
WORKDIR /app

# Keep the container running in the background
CMD ["tail", "-f", "/dev/null"]
