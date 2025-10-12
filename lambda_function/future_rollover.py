import os
from datetime import datetime
from decimal import Decimal

import boto3
import shioaji
from dotenv import load_dotenv
from shioaji.constant import Action
from shioaji.contracts import Future

from core.strategy import LowerThanMedianOfXDaysStrategy, MustBuyIfSettlementThisWeekStrategy
from future.core import login, find_target_future_contract, get_future_contracts, is_hold_future, get_latest_tick
from future.future_dao import FutureDao
from future.trading import trade


def get_latest_future_contract(future_contract_dict: dict):
    latest_future_contract = find_target_future_contract(future_contract_dict, "MXFR1")
    next_two_month_future_contract = find_target_future_contract(future_contract_dict, "MXFR2")

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


def is_buy_by_strategies(strategies, recently_future_contract, next_two_month_future_contract):
    for strategy in strategies:
        is_buy = strategy.is_buy(recently_future_contract, next_two_month_future_contract)
        print(f"is the strategy [{strategy.strategy_name}] calling for a buy?: [{is_buy}]")

        if is_buy:
            return True

    return False


def handler(event, context=None):
    simulation = event.get("simulation", "True") == "True"
    print(f"simulation is {simulation}")

    load_dotenv()

    api = login(simulation)

    dynamodb_client = boto3.resource("dynamodb")

    future_contract_dict = get_future_contracts(api)
    recently_future_contract, next_two_month_future_contract = get_latest_future_contract(future_contract_dict)

    recently_future_tick = get_latest_tick(api, recently_future_contract)
    next_two_month_future_tick = get_latest_tick(api, next_two_month_future_contract)

    if recently_future_tick.close:
        recently_future_contract.reference = recently_future_tick.close[0]

    if next_two_month_future_tick.close:
        next_two_month_future_contract.reference = next_two_month_future_tick.close[0]

    print(f"the latest future contract:")
    print(recently_future_contract)

    print(f"the next two month future contract:")
    print(next_two_month_future_contract)

    if not simulation:
        save_contracts(dynamodb_client, recently_future_contract, next_two_month_future_contract)

    if is_hold_future(api, next_two_month_future_contract):
        print("holding the next two month future contract, end the lambda")
        return

    check_days = os.getenv("check_days", 10)
    strategies = [MustBuyIfSettlementThisWeekStrategy(), LowerThanMedianOfXDaysStrategy(dynamodb_client, check_days)]
    is_buy = is_buy_by_strategies(strategies, recently_future_contract, next_two_month_future_contract)
    print(f"do i rollover future? -> {is_buy}")

    if is_buy:
        if is_hold_future(api, recently_future_contract):
            trade(api, Action.Sell, recently_future_contract)
            trade(api, Action.Buy, next_two_month_future_contract)
        else:
            print("not holding the recent future contract, end the trade")

    api.logout()


if __name__ == '__main__':
    handler({}, None)
