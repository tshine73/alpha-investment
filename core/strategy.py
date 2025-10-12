from datetime import datetime, timedelta

import pandas as pd

from future.future_dao import FutureDao
from future_utils.date_utils import get_weekday_name


class Strategy:
    def __init__(self):
        self.strategy_name = type(self).__name__

    def is_buy(self, latest_future_contract, next_two_month_future_contract) -> bool:
        pass

    def log(self, message):
        print(f"[{self.strategy_name}] - {message}")


class LowerThanStrategy(Strategy):
    def __init__(self, client, check_days=10):
        super().__init__()
        self.future_dao = FutureDao(client)
        self.check_days = check_days
        self.log(f"check days is {check_days}")

    def get_history_references(self, latest_future_contract, next_two_month_future_contract):
        latest_future_df = pd.DataFrame(self.future_dao.query_by_code(latest_future_contract.code))
        next_two_month_future_df = pd.DataFrame(self.future_dao.query_by_code(next_two_month_future_contract.code))

        combined_df = pd.merge(latest_future_df, next_two_month_future_df, on="update_time", suffixes=('_l', '_r'))

        combined_df["backwardation"] = combined_df["reference_r"] - combined_df["reference_l"]
        combined_df["updated_date"] = pd.to_datetime(combined_df["update_time"], format='%Y-%m-%d %H:%M:%S').dt.date

        backwardation_df = combined_df[["updated_date", "backwardation"]]

        return backwardation_df

    def group_backwardation(self, backwardation_df):
        groupby_df = backwardation_df.groupby("updated_date").agg(
            count_backwardation=('backwardation', 'count'),
            min_backwardation=('backwardation', 'min'),
            max_backwardation=('backwardation', 'max')
        )

        self.log(f"distinct quote date count: {len(groupby_df)}")
        self.log("statistics of daily backwardation:")
        self.log(groupby_df)

        return groupby_df

    def is_buy(self, latest_future_contract, next_two_month_future_contract) -> bool:
        backwardation_df = self.get_history_references(latest_future_contract, next_two_month_future_contract)
        groupby_df = self.group_backwardation(backwardation_df)

        if len(groupby_df) > self.check_days:
            history_backwardation = self.get_specific_backwardation(backwardation_df)
            current_backwardation = next_two_month_future_contract.reference - latest_future_contract.reference
            self.log(f"history backwardation: {history_backwardation}")
            self.log(f"current backwardation: {current_backwardation}")

            return current_backwardation <= history_backwardation
        else:
            self.log(f"not enough quote data dates: {len(groupby_df) - 1}, need {self.check_days}")
            return False

    def get_specific_backwardation(self, backwardation_series) -> int:
        pass


class LowerThanMinOfXDaysStrategy(LowerThanStrategy):
    def get_specific_backwardation(self, backwardation_df) -> int:
        return backwardation_df["backwardation"].min()


class LowerThanMedianOfXDaysStrategy(LowerThanStrategy):
    def get_specific_backwardation(self, backwardation_df) -> int:
        return self.group_backwardation(backwardation_df)["min_backwardation"].median()


class MustBuyIfSettlementThisWeekStrategy(Strategy):
    def is_settlement_week(self, date) -> bool:
        first_day_of_month = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if first_day_of_month.weekday() <= 2:
            plus_weeks = 2
        else:
            plus_weeks = 3

        third_week = first_day_of_month + timedelta(weeks=plus_weeks)
        first_day_of_third_week = third_week - timedelta(third_week.weekday())
        wednesday_of_third_week = first_day_of_third_week + timedelta(days=2)

        return first_day_of_third_week <= date <= wednesday_of_third_week

    def is_buy(self, latest_future_contract, next_two_month_future_contract) -> bool:
        today = datetime.today()
        weekday_name = get_weekday_name(today.weekday())
        is_settlement_this_week = self.is_settlement_week(datetime.today())

        self.log(f"today is {weekday_name}, is settlement this week [{is_settlement_this_week}]")

        return is_settlement_this_week
