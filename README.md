# alpha-investment

### install library
```bash
pip install -r requirements.txt
```

### follow the blog post to setup API key and certification


### add `.env` file
please setup `.env` file in project root

```editorconfig
API_KEY=
SECRET_KEY=
CA_CERT_PATH=
CA_PASSWORD=
```

### run
```bash
cd ./alpha-investment
PYTHONPATH=./ python ./future/get_future_index.py
```