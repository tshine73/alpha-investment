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



def trade(api, trade_type: TradeType, price: Price, future_contract: Future):
    trade = api.update_status(api.futopt_account)
    print(trade)
    #
    # contract = min(
    #     [
    #         x for x in api.Contracts.Futures.TXF
    #         if x.code[-2:] not in ["R1", "R2"]
    #     ],
    #     key=lambda x: x.delivery_date
    # )

    # price (float or int): 價格
    # quantity (int): 委託數量
    # action (str): {Buy: 買, Sell: 賣}
    # price_type (str): {LMT: 限價, MKT: 市價, MKP: 範圍市價}
    # order_type (str): 委託類別 {ROD, IOC, FOK}
    # octype (str): {Auto: 自動, New: 新倉, Cover: 平倉, DayTrade: 當沖}
    # account (:obj:Account): 下單帳號
    # ca (binary): 憑證

    # 期貨委託單 - 請修改此處
    # order = api.Order(
    #     action=sj.constant.Action.Buy,  # 買賣別
    #     price=24000,  # 價格
    #     quantity=1,  # 數量
    #     price_type=sj.constant.FuturesPriceType.LMT,  # 委託價格類別
    #     order_type=sj.constant.OrderType.ROD,  # 委託條件
    #     octype=sj.constant.FuturesOCType.Auto,  # 倉別
    #     account=api.futopt_account  # 下單帳號
    # )
    #
    # # 下單
    # trade = api.place_order(contract, order)
    # print(trade)
    #
    #
    #
    #
    #
    # # PendingSubmit: 傳送中
    # # PreSubmitted: 預約單
    # # Submitted: 傳送成功
    # # Failed: 失敗
    # # Cancelled: 已刪除
    # # Filled: 完全成交
    # # Filling: 部分成交
    #
    # api.update_order(trade=trade, price=14450)
    # api.update_status(api.futopt_account)
    # trade
    #
    # is trade_type == TradeType.buy and
    #
    # trade = api.Order(
    #     action=sj.constant.Action.Buy,  # 買賣別
    #     price=23000,  # 價格
    #     quantity=1,  # 數量
    #     price_type=sj.constant.FuturesPriceType.LMT,  # 委託價格類別
    #     order_type=sj.constant.OrderType.ROD,  # 委託條件
    #     octype=sj.constant.FuturesOCType.Auto,  # 倉別
    #     account=api.futopt_account  # 下單帳號
    # )
    #
    # pass



def handler(event, context=None):
    api = login(simulation=False)

    future_contract_dict = init_future_contracts(api)
    contract = find_target_future_contract(future_contract_dict, "MXFR1")

    trade(api, TradeType.buy, Price.market, contract)




if __name__ == '__main__':
    handler(None)
