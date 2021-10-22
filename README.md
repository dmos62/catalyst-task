# Catalyst task

To build the docker image:

```
docker build -t littlejohn:latest .
```

To run the docker image:

```
docker run -p 5000:5000 littlejohn
```

To run the tests:

```
pip3 install -r requirements.txt
pip3 install pytest
pytest -v
```

To run the app locally:

```
pip3 install -r requirements.txt
python3 main.py
```

To make a query:

```
USER_TOKEN=123
curl "127.0.0.1:5000/tickers" -u "$USER_TOKEN:"
```
