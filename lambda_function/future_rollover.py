import time
from datetime import datetime
from decimal import Decimal

import boto3
import shioaji
from shioaji.contracts import Future

from future.core import login, find_target_future_contract, init_future_contracts
from future.future_dao import FutureDao


def get_latest_future_contract(future_contract_dict: dict):
    latest_future_contract = find_target_future_contract(future_contract_dict, "MXFR1")
    next_two_month_future_contract = find_target_future_contract(future_contract_dict, "MXFR2")
    for i in future_contract_dict:
        print(future_contract_dict[i])
    # latest_future_contract = find_target_future_contract(future_contract_dict, "MXFPMI5")
    # next_two_month_future_contract = find_target_future_contract(future_contract_dict, "MXFPMJ5")

    print(f"the latest future contract:")
    print(latest_future_contract)

    print(f"the next two month future contract:")
    print(next_two_month_future_contract)

    return latest_future_contract, next_two_month_future_contract


def clean(*contracts: Future):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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


def quote(api, future_contract: Future):
    api.quote.subscribe(
        future_contract,
        quote_type=shioaji.constant.QuoteType.Tick,
        version=shioaji.constant.QuoteVersion.v1,
    )


def handler(event, context=None):
    simulation = event.get("simulation", "True") == "True"

    api = login(simulation)

    future_contract_dict = init_future_contracts(api)
    latest_future_contract, next_two_month_future_contract = get_latest_future_contract(future_contract_dict)
    cleaned_contracts = clean(latest_future_contract, next_two_month_future_contract)
    quote(api, latest_future_contract)
    # save(*cleaned_contracts)

    i = 0
    while i < 100:
        time.sleep(1)
        i += 1

    api.logout()


if __name__ == '__main__':
    handler({}, None)
