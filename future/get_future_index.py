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


def get_latest_future_contract(future_contract_dict: dict):
    latest_future_contract = find_target_future_contract(future_contract_dict, "MXFR1")
    next_two_month_future_contract = find_target_future_contract(future_contract_dict, "MXFR2")

    print(f"the latest future contract:")
    print(latest_future_contract)

    print(f"the next two month future contract:")
    print(next_two_month_future_contract)

    return latest_future_contract, next_two_month_future_contract


def is_backwardation(latest_future_contract: Future, next_two_month_future_contract: Future):
    backwardation = next_two_month_future_contract.reference - latest_future_contract.reference
    print(
        f"the {latest_future_contract.name} -> {next_two_month_future_contract.name} backwardation point is {backwardation}")


def clean(*contracts: Future):
    now = format_date(datetime.now())
    cleaned_contracts = []
    for contract in contracts:
        cleaned_contract = {
            "code": contract.code,
            "symbol": contract.symbol,
            "name": contract.name,
            "category": contract.category,
            "delivery_month": contract.delivery_month,
            "delivery_date": contract.delivery_date,
            "underlying_kind": contract.underlying_kind,
            "unit": contract.unit,
            "reference": Decimal(contract.reference),
            "update_time": now
        }
        cleaned_contracts.append(cleaned_contract)

    return cleaned_contracts


def save(*contracts: Future):
    dynamodb_client = boto3.resource("dynamodb")
    future_dao = FutureDao(dynamodb_client)
    future_dao.write_batch(list(contracts))
    print("save future contract to dynamodb success")


def handler(event, context=None):
    load_dotenv()
    api = login()

    future_contract_dict = init_future_contracts(api)
    latest_future_contract, next_two_month_future_contract = get_latest_future_contract(future_contract_dict)
    is_backwardation(latest_future_contract, next_two_month_future_contract)
    cleaned_contracts = clean(latest_future_contract, next_two_month_future_contract)
    save(*cleaned_contracts)


if __name__ == '__main__':
    handler(None)
