from enum import Enum


class StrategyModel(str, Enum):
    trade_if_the_backwardation_below_its_historical_benchmark = 's1'

