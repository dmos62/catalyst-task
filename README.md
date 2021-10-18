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
