from aws_cdk import (
    aws_s3 as s3,
    NestedStack,
    RemovalPolicy,
)

from constructs import Construct


class S3Module(NestedStack):
    def _create_s3_bucket(self):
        return s3.Bucket(
            self, 'bucket',
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = self._create_s3_bucket()
