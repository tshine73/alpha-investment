import time
from datetime import datetime
from decimal import Decimal

import boto3
import shioaji
from shioaji.contracts import Future

from core.strategy import LowerThanMinOfXDaysStrategy
from future.core import login, find_target_future_contract, init_future_contracts, is_hold_future
from future.future_dao import FutureDao
from future.trading import trade
from model.constant import TradeType, Price


def get_latest_future_contract(future_contract_dict: dict):
    latest_future_contract = find_target_future_contract(future_contract_dict, "MXFR1")
    next_two_month_future_contract = find_target_future_contract(future_contract_dict, "MXFR2")

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


def save_contracts(dynamodb_client, *contracts: Future):
    clean_contracts = clean(*contracts)

    future_dao = FutureDao(dynamodb_client)
    future_dao.write_batch(list(clean_contracts))
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

    dynamodb_client = boto3.resource("dynamodb")

    future_contract_dict = init_future_contracts(api)
    recently_future_contract, next_two_month_future_contract = get_latest_future_contract(future_contract_dict)

    # save_contracts(dynamodb_client, recently_future_contract, next_two_month_future_contract)

    if is_hold_future(api, next_two_month_future_contract):
        print("holding the next two month future contract, end the lambda")
        return

    strategy = LowerThanMinOfXDaysStrategy(dynamodb_client)
    is_buy = strategy.is_buy(recently_future_contract, next_two_month_future_contract)
    print(f"the strategy result is: {is_buy}")

    if is_buy:
        if is_hold_future(api, recently_future_contract):
            trade(api, TradeType.sale, Price.market, recently_future_contract)
            trade(TradeType.buy, Price.market, next_two_month_future_contract)
        else:
            print("not holding the recent future contract, end the trade")

    api.logout()


if __name__ == '__main__':
    handler({}, None)
