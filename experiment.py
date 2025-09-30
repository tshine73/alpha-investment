import boto3
import pandas as pd

from future.future_dao import FutureDao


def main():
    import pandas as pd

    # Sample DataFrame
    data = {'Category': ['A', 'B', 'A', 'C', 'B', 'A', 'C'],
            'Value1': [10, 20, 15, 30, 25, 12, 35],
            'Value2': [1, 5, 2, 8, 6, 3, 9]}
    df = pd.DataFrame(data)

    # Group by 'Category' and calculate count and min for 'Value1' and 'Value2'
    result = df.groupby('Category').agg(
        count_Value1=('Value1', 'count'),
        min_Value1=('Value1', 'min'),
        count_Value2=('Value2', 'count'),
        min_Value2=('Value2', 'min')
    )

    print(result)
    
    


    

if __name__ == '__main__':
    main()