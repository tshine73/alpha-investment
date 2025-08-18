from datetime import datetime
from decimal import Decimal

import boto3
import shioaji as sj
from shioaji.contracts import Future

from core.strategy import Strategy
from future.core import login, find_target_future_contract, init_future_contracts
from future.future_dao import FutureDao
from future.trading import trade
from model.constant import StrategyModel, TradeType, Price
from utils.date_utils import format_date


def find_target_future(latest_future_contract, next_two_month_future_contract):
    return None

def notify():
    pass

def is_buy(strategy: Strategy, latest_future_contract, next_two_month_future_contract):
    # backwardation = next_two_month_future_contract.reference - latest_future_contract.reference
    # print(
    #     f"the {latest_future_contract.name} -> {next_two_month_future_contract.name} backwardation point is {backwardation}")
    #
    # if strategy == StrategyModel.trade_if_the_backwardation_below_its_historical_benchmark:

    single, message = strategy.is_buy()
    print(message)
    if (single):
        contract = find_target_future(latest_future_contract, next_two_month_future_contract)
        trade(TradeType.buy, Price.market, contract)
        notify()