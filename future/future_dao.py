import logging

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class FutureDao:
    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.table = dyn_resource.Table("future")

    def write_batch(self, futures: list):
        try:
            with self.table.batch_writer() as writer:
                for future in futures:
                    writer.put_item(Item=future)
        except ClientError as err:
            logger.error(
                "Couldn't load data into table %s. Here's why: %s: %s",
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def query_by_code(self, code: str):
        try:
            response = self.table.query(
                KeyConditionExpression=Key('code').eq(code),
            )
            return response['Items']
        except ClientError as err:
            logger.error(
                "Couldn't query table %s. Here's why: %s: %s",
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
