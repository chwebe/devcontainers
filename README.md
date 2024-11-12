docker buildx build --platform linux/amd64,linux/arm64 -t chwebe/python-binance --push .
docker run -it -d --name python-binance-project -v ./app:/app python-binance:1.0
