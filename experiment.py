import boto3
import pandas as pd

from future.future_dao import FutureDao


def main():
    dynamodb_client = boto3.resource("dynamodb")
    future_dao = FutureDao(dynamodb_client)

    latest = future_dao.query_by_code("MXFI5")
    next_two_month = future_dao.query_by_code("MXFJ5")
    latest_df = pd.DataFrame(latest)
    next_two_month_df = pd.DataFrame(next_two_month)
    print(latest[0])
    print(len(latest_df))
    print(len(next_two_month_df))
    combined_df = pd.merge(latest_df, next_two_month_df, on="update_time", suffixes=('_l', '_r'))

    print(combined_df)
    print(combined_df.dtypes)

    combined_df["backwardation"] = combined_df["reference_r"] - combined_df["reference_l"]
    combined_df["updated_date"] = pd.to_datetime(combined_df["update_time"], format='%Y-%m-%d %H:%M:%S').dt.date



    df = combined_df[["updated_date", "backwardation"]]

    count_df = df.groupby("updated_date").count().rename(columns={"backwardation": "backwardation_count"})
    print(len(count_df))
    print(count_df)

    distinct_dates_count = df["updated_date"].nunique()
    print(f"Distinct updated_date count: {distinct_dates_count}")
    
    
    
    print(df)
    print(df.dtypes)
    
    min_backwardation = df["backwardation"].min()
    print(f"Minimum backwardation: {min_backwardation}")
    print(type(min_backwardation))

    print(min_backwardation > 0)
    
    


    

if __name__ == '__main__':
    main()