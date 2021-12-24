## Developing
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

pip install requests
pip freeze > requirements.txt
```

```sh
export TCP_IP_ADDRESS_BIND=0.0.0.0 
export TCP_PORT_NUMBER=8108
export TCP_SERVER_TIMEOUT=20
export APIGW_BASE_URL="<YOUR APIGW ROUTE>"

python tcp_server.py
```

```sh
export TCP_SERVER_IP_ADDRESS=0.0.0.0 
export TCP_PORT_NUMBER=8108

python tcp_client.py
```