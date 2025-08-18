class Strategy:
    def is_buy(self, latest_future_contract, next_two_month_future_contract) -> (bool, str):
        pass


class DefaultStrategy(Strategy):
    def is_buy(self, latest_future_contract, next_two_month_future_contract) -> (bool, str):
        return True, "default strategy"
