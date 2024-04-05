from aws_cdk import (
    aws_iam as iam,
    NestedStack,
)

from constructs import Construct

class IAMModule(NestedStack):
    def __create_ecs_instance_profile(self):
        role = iam.Role(
            self, 'ecsRole',
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(
                    self, 'ECSRoleS3',
                    'arn:aws:iam::aws:policy/AmazonS3FullAccess'
                ),
                iam.ManagedPolicy.from_managed_policy_arn(
                    self, 'ECSRoleEC2',
                    'arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role'
                )
            ]
        )

        instance_profile = iam.CfnInstanceProfile(self, 'ecsinstanceprofile', roles=[role.role_name])
        instance_profile.node.add_dependency(role)

        return instance_profile

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.instance_profile = self.__create_ecs_instance_profile()
