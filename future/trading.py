import os
from datetime import datetime
from decimal import Decimal

import boto3
import shioaji as sj
from dotenv import load_dotenv
from shioaji.contracts import Future

from future.core import login, find_target_future_contract, init_future_contracts
from future.future_dao import FutureDao
from model.constant import TradeType, Price
from utils.date_utils import format_date


def trade(api, trade_type: TradeType, price: Price, future_contract: Future):
    pass



def handler(event, context=None):
    api = login(simulation=False)

    print(api.get_ca_expiretime("F126811241"))


    future_contract_dict = init_future_contracts(api)
    contract = find_target_future_contract(future_contract_dict, "MXFR1")

    #
    # contract = min(
    #     [
    #         x for x in api.Contracts.Futures.TXF
    #         if x.code[-2:] not in ["R1", "R2"]
    #     ],
    #     key=lambda x: x.delivery_date
    # )

    # 期貨委託單 - 請修改此處
    order = api.Order(
        action=sj.constant.Action.Buy,  # 買賣別
        price=23000,  # 價格
        quantity=1,  # 數量
        price_type=sj.constant.FuturesPriceType.LMT,  # 委託價格類別
        order_type=sj.constant.OrderType.ROD,  # 委託條件
        octype=sj.constant.FuturesOCType.Auto,  # 倉別
        account=api.futopt_account  # 下單帳號
    )

    # 下單
    trade = api.place_order(contract, order)
    print(trade)


if __name__ == '__main__':
    handler(None)
