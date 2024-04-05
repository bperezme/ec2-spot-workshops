from aws_cdk import (
    Stack,
    CfnOutput
)

from constructs import Construct
from .modules import *


class PipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_module = S3Module(self, 'S3Module')
        lambda_module = LambdaModule(self, 'LambdaModule', s3_module.bucket)
        sf_module = StepFunctionsModule(self, 'StepFunctionsModule', s3_module.bucket, lambda_module.preprocessing_func)

        ec2_module = EC2Module(self, 'EC2Module')
        ecr_module = ECRModule(self, 'ECRModule')
        iam_module = IAMModule(self, 'IAMModule')

        CfnOutput(self, 'PreprocessingLambda', value=lambda_module.preprocessing_func.function_name)
        CfnOutput(self, 'Subnet1', value=ec2_module.vpc.select_subnets().subnets[0].subnet_id)
        CfnOutput(self, 'Subnet2', value=ec2_module.vpc.select_subnets().subnets[1].subnet_id)
        CfnOutput(self, 'LaunchTemplateName', value='RenderingWithBatch')
        CfnOutput(self, 'RepositoryName', value=ecr_module.repository.repository_name)
        CfnOutput(self, 'ECSInstanceProfile', value=iam_module.instance_profile.attr_arn)
        CfnOutput(self, 'BucketName', value=s3_module.bucket.bucket_name)
        CfnOutput(self, 'BlendFileName', value='blendfile.blend')
        CfnOutput(self, 'StateMachineArn', value=sf_module.state_machine.state_machine_arn)
