from datetime import datetime

from shioaji.constant import Status, Action, FuturesPriceType, FuturesOCType, OrderType
from shioaji.contracts import Future

from future.core import login, find_target_future_contract, init_future_contracts, is_hold_future


###
# Status
## PendingSubmit: 傳送中
## PreSubmitted: 預約單
## Submitted: 傳送成功
## Failed: 失敗
## Cancelled: 已刪除
## Filled: 完全成交
## Filling: 部分成交


# api.Order(
## price (float or int): 價格
## quantity (int): 委託數量
## action (str): {Buy: 買, Sell: 賣}
## price_type (str): {LMT: 限價, MKT: 市價, MKP: 範圍市價}
## order_type (str): 委託類別 {ROD, IOC, FOK}
## octype (str): {Auto: 自動, New: 新倉, Cover: 平倉, DayTrade: 當沖}
## account (:obj:Account): 下單帳號
## ca (binary): 憑證
# )
###
def trade(api, action: Action, contract: Future):
    api.update_status(api.futopt_account)
    all_trades = api.list_trades()

    today = datetime.now().strftime('%Y-%m-%d')
    trades = [trade for trade in all_trades if
              (trade.status.status == Status.Submitted or trade.status.status == Status.PreSubmitted)
              and trade.status.order_datetime.strftime('%Y-%m-%d') == today
              and trade.contract.code == contract.code and trade.order.action == action]

    if trades:
        print(f"found [{len(trades)}] submitted trades need to be update price")
        for trade in trades:
            new_price = contract.reference
            api.update_order(
                trade,
                price=new_price
            )
            original_price = trade.status.modified_price or trade.order.price
            print(f"original price: {original_price}, updated price: {new_price}")
    else:
        print("no submitted trade, place order")

        if (action == Action.Buy and not is_hold_future(api, contract)) or \
                (action == Action.Sell and is_hold_future(api, contract)):
            order = api.Order(
                action=action,  # 買賣別
                price=contract.reference,  # 價格
                quantity=1,  # 數量
                price_type=FuturesPriceType.LMT,  # 委託價格類別
                order_type=OrderType.ROD,  # 委託條件
                octype=FuturesOCType.Auto,  # 倉別
                account=api.futopt_account  # 下單帳號
            )

            trade = api.place_order(contract, order)
            print("place order success")
            print(trade)
        else:
            if action == Action.Buy:
                print(f"you are holding future contract {contract.name}, does not need to buy")
            else:
                print(f"you are not holding future contract {contract.name}, does not need to sell")


def handler(event, context=None):
    api = login(simulation=False)

    future_contract_dict = init_future_contracts(api)
    contract = find_target_future_contract(future_contract_dict, "MXFR1")

    trade(api, Action.Buy, contract)


if __name__ == '__main__':
    handler(None)
