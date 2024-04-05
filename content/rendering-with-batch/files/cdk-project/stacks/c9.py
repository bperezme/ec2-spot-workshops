from aws_cdk import (
    Stack,
    aws_cloud9 as cloud9,
    aws_iam as iam
)

from constructs import Construct
from cdk_use_cases.custom_cloud9_ssm import CustomCloud9Ssm


class C9EnvStack(Stack):
    def __create_environment(self):
        env = CustomCloud9Ssm(
            self, 'CustomCloud9Ssm',
            cloud9_ec2_props=cloud9.CfnEnvironmentEC2Props(
                image_id='amazonlinux-2-x86_64',
                instance_type='m5.large'
            )
        )

        env.ec2_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                resources=['*'],
                actions=[
                    "batch:DescribeJobQueues",
                    "batch:CreateComputeEnvironment",
                    "batch:DeleteComputeEnvironment",
                    "batch:SubmitJob",
                    "batch:UpdateComputeEnvironment",
                    "batch:ListJobs",
                    "batch:DescribeComputeEnvironments",
                    "batch:DeregisterJobDefinition",
                    "batch:CreateJobQueue",
                    "batch:DescribeJobs",
                    "batch:RegisterJobDefinition",
                    "batch:DescribeJobDefinitions",
                    "batch:DeleteJobQueue",
                    "batch:UpdateJobQueue",
                    "cloudformation:DescribeStacks",
                    "s3:PutObject",
                    "s3:ListBucket",
                    "s3:DeleteObject",
                    "ecr:*",
                    "states:StartExecution",
                    "iam:PassRole"
                ]
            )
        )

        # Add a step in SSM doc that deploys the CDK project with all the resources
        with open('assets/deploy_rendering_stack.yml') as fd:
            step = fd.read()

        env.add_document_steps(step)

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.__create_environment()
