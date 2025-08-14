import os
from datetime import datetime
from decimal import Decimal

import boto3
import shioaji as sj
from dotenv import load_dotenv
from shioaji.contracts import Future

from future.future_dao import FutureDao
from utils.date_utils import format_date



def login():
    load_dotenv()

    api = sj.Shioaji(simulation=True)  # 模擬模式
    accounts = api.login(
        api_key=os.getenv("API_KEY"),
        secret_key=os.getenv("SECRET_KEY"),
        fetch_contract=False
    )

    print(accounts)

    api.activate_ca(
        ca_path=os.getenv("CA_CERT_PATH"),
        ca_passwd=os.getenv("CA_PASSWORD"),
    )
    print("login and activate ca success")

    return api

def init_future_contracts(api: sj.Shioaji):
    api.fetch_contracts(contract_download=True, contracts_timeout=3000)
    future_contract_dict = {}
    for futures in api.Contracts.Futures:
        for future in futures:
            future_contract_dict[future.code] = future

    return future_contract_dict


def find_target_future_contract(future_contract_dict, code: str):
    contract = future_contract_dict[code]
    while contract.target_code != "":
        contract = future_contract_dict[contract.target_code]

    return contract