import os

from dotenv import load_dotenv

import shioaji as sj

from future.get_future_index import login


def trade_stock(api: sj.Shioaji):
    contract = api.Contracts.Stocks.TSE["2890"]

    # 證券委託單 - 請修改此處
    order = api.Order(
        price=21,  # 價格
        quantity=1,  # 數量
        action=sj.constant.Action.Buy,  # 買賣別
        price_type=sj.constant.StockPriceType.LMT,  # 委託價格類別
        order_type=sj.constant.OrderType.ROD,  # 委託條件
        account=api.stock_account  # 下單帳號
    )

    # 下單
    trade = api.place_order(contract, order)
    print(trade)


def trade_future(api: sj.Shioaji):
    # 商品檔 - 近月台指期貨, 請修改此處
    contract = min(
        [
            x for x in api.Contracts.Futures.TXF
            if x.code[-2:] not in ["R1", "R2"]
        ],
        key=lambda x: x.delivery_date
    )

    print(contract)
    # 期貨委託單 - 請修改此處
    order = api.Order(
        action=sj.constant.Action.Buy,  # 買賣別
        price=15000,  # 價格
        quantity=1,  # 數量
        price_type=sj.constant.FuturesPriceType.LMT,  # 委託價格類別
        order_type=sj.constant.OrderType.ROD,  # 委託條件
        octype=sj.constant.FuturesOCType.Auto,  # 倉別
        account=api.futopt_account  # 下單帳號
    )

    # 下單
    trade = api.place_order(contract, order)
    print(trade)


def list_app_future_product(api: sj.Shioaji):
    api.fetch_contracts(contract_download=True, contracts_timeout=3000)

    for future in api.Contracts.Futures:
        for f in future:
            print(f)


if __name__ == '__main__':
    load_dotenv()
    api = login()

    list_app_future_product(api)
