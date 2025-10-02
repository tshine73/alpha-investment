import pandas as pd

from future.future_dao import FutureDao


class Strategy:
    def __init__(self, client):
        self.future_dao = FutureDao(client)

    def is_buy(self, latest_future_contract, next_two_month_future_contract) -> bool:
        pass


class LowerThanMinOfXDaysStrategy(Strategy):
    def __init__(self, client, check_days=10):
        super().__init__(client)
        self.check_days = check_days
        print(f"init strategy: LowerThanMinOfXDaysStrategy, the check days {check_days}")

    def is_buy(self, latest_future_contract, next_two_month_future_contract) -> bool:
        latest_future_df = pd.DataFrame(self.future_dao.query_by_code(latest_future_contract.code))
        next_two_month_future_df = pd.DataFrame(self.future_dao.query_by_code(next_two_month_future_contract.code))

        combined_df = pd.merge(latest_future_df, next_two_month_future_df, on="update_time", suffixes=('_l', '_r'))

        combined_df["backwardation"] = combined_df["reference_r"] - combined_df["reference_l"]
        combined_df["updated_date"] = pd.to_datetime(combined_df["update_time"], format='%Y-%m-%d %H:%M:%S').dt.date

        backwardation_df = combined_df[["updated_date", "backwardation"]]

        groupby_df = backwardation_df.groupby("updated_date").agg(
            count_backwardation=('backwardation', 'count'),
            min_backwardation=('backwardation', 'min'),
            max_backwardation=('backwardation', 'max')
        )

        print(f"distinct quote date count: {len(groupby_df)}")
        print("statistics of daily backwardation:")
        print(groupby_df)

        if len(groupby_df) > self.check_days:
            history_min_backwardation = backwardation_df["backwardation"].min()
            current_backwardation = next_two_month_future_contract.reference - latest_future_contract.reference
            print("history min backwardation: ", history_min_backwardation)
            print("current backwardation: ", current_backwardation)

            return current_backwardation <= history_min_backwardation
        else:
            print(f"not enough quote data dates: {len(groupby_df) - 1}, need {self.check_days}")
            return False
