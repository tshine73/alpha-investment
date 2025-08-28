# alpha-investment

## Prepare

### install library

```bash
pip install -r requirements.txt
```

### follow the blog post to setup API key and certification

https://tshine73.blog/category/system/%e9%9b%a3%e9%81%93%e5%8f%b0%e6%8c%87%e6%9c%9f%e9%83%bd%e4%b8%8d%e6%9c%83%e6%9c%89%e9%80%86%e5%83%b9%e5%b7%ae%e4%ba%86%e5%97%8e/

### add `.env` file

please setup `.env` file in project root

```editorconfig
API_KEY = SECRET_KEY=

CA_CERT_PATH = CA_PASSWORD=
```

### run

```bash
cd ./alpha-investment
PYTHONPATH=./ python ./future/get_future_index.py
```

pip install shioaji==1.2.5 --target ./package
pip install python-dotenv==1.0.1 pydantic==2.11.7 --target ./package --platform manylinux2014_x86_64 --only-binary=:all:
pip install -r ../requirements.txt --target ./package 
pip install python-dotenv==1.0.1 shioaji==1.2.5 --target ./package
pip install python-dotenv==1.0.1 shioaji==1.2.5 --target ./package --platform manylinux2014_x86_64 --only-binary=:all:


pip install -r ../requirements.txt --target ./package

## deploy

```shell
rm deployment_package.zip
mkdir package
pip install shioaji==1.2.7 python-dotenv==1.0.1 pydantic==2.11.5 --target ./package
cp -r ../lambda_function ./package/
rm -rf ./package/lambda_function/__pycache__
cp -r ../utils ./package/
rm -rf ./package/utils/__pycache__  
cp -r ../model ./package/
rm -rf ./package/model/__pycache__
cp -r ../future ./package/
rm -rf ./package/future/__pycache__
cp -r ../core ./package/
rm -rf ./package/core/__pycache__
cp -r ../resources ./package/
cp .env ./package
cd package
zip -r ../deployment_package.zip .
cd ..
rm -rf package
```