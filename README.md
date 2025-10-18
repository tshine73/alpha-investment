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

## deploy
### create EC2 with os Amazon Linux, and then install python 3.12
```bash
sudo yum install -y python3.12
sudo yum install git -y
sudo yum install -y python3-pip
sudo yum install -y zip
python3.12 -m venv deployment_env
source deployment_env/bin/activate
cd ~
git clone https://github.com/tshine73/alpha-investment.git 
```

### open new terminal, copy .env and Sinopac.pfx to ec2 
```bash
scp -i ~/.ssh/tshine73.pem .env ec2-user@35.92.138.15:~/alpha-investment/deployment/
scp -i ~/.ssh/tshine73.pem ./alpha-investment/resources/Sinopac.pfx ec2-user@52.32.87.1:~/alpha-investment/resources/
```

### ssh to ec2 and package
```shell
git pull
source deployment_env/bin/activate
cd deployment
rm deployment_package.zip
mkdir package
pip install shioaji==1.2.7 python-dotenv==1.0.1 pydantic==2.11.5 --target ./package
cp -r ../lambda_function ./package/
rm -rf ./package/lambda_function/__pycache__
cp -r ../future_utils ./package/
rm -rf ./package/future_utils/__pycache__  
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

### download the zip and deploy to lambda
```bash
scp -i ~/.ssh/tshine73.pem ec2-user@34.222.45.92:/home/ec2-user/alpha-investment/deployment/deployment_package.zip ./
```

## prepare pandas layer for lambda
```bash
cd deployment
rm -rf pandas-manual-package
rm pandas-manual-package.zip
mkdir -p pandas-manual-package/python/lib/python3.12/site-packages
pip install pandas==2.3.2 --target ./pandas-manual-package/python/lib/python3.12/site-packages --platform manylinux2014_x86_64 --only-binary=:all:
rm -rf pandas-manual-package/python/lib/python3.12/site-packages/pandas/tests
cd pandas-manual-package
zip -r ../pandas-manual-package.zip .
cd ..
```