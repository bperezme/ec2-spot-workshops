from aws_cdk import (
    aws_ecr as ecr,
    RemovalPolicy,
    NestedStack,
)

from constructs import Construct

class ECRModule(NestedStack):
    def __create_repository(self):
        return ecr.Repository(
            self, 'repository',
            repository_name='rendering-with-batch',
            removal_policy=RemovalPolicy.DESTROY
        )

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.repository = self.__create_repository()
