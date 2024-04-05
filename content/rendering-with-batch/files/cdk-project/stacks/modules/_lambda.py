from aws_cdk import (
    aws_lambda as _lambda,
    NestedStack,
    Duration,
)

from constructs import Construct


class LambdaModule(NestedStack):
    __RUNTIME = _lambda.Runtime.PYTHON_3_11

    def __create_preprocessing_func(self, bucket):
        with open('assets/preprocessing.py') as fd:
            code = fd.read()

            function = _lambda.Function(
                self, 'Preprocessing',
                runtime=self.__RUNTIME,
                code=_lambda.Code.from_inline(code),
                handler='index.handler',
                timeout=Duration.minutes(5)
            )

            bucket.grant_read(function)

            return function

    def __init__(self, scope: Construct, construct_id: str, bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.preprocessing_func = self.__create_preprocessing_func(bucket)
