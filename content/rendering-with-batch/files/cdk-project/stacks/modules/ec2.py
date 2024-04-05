from aws_cdk import (
    aws_ec2 as ec2,
    NestedStack
)

from constructs import Construct


class EC2Module(NestedStack):
    def __create_vpc(self):
        vpc = ec2.Vpc(
            self, "Vpc",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    cidr_mask=24,
                    name="RenderingWithBatch",
                    subnet_type=ec2.SubnetType.PUBLIC
                )
            ]
        )

        return vpc

    def __create_launch_template(self, vpc):
        security_group = ec2.SecurityGroup(
            self, 'securityGroup',
            security_group_name="RenderingWithBatch",
            allow_all_outbound=True,
            vpc=vpc
        )
        security_group.node.add_dependency(vpc)

        # Read the user data from the text file
        with open('assets/launch-template-user-data.txt') as fd:
            user_data = fd.read()

            launch_template = ec2.LaunchTemplate(
                self, 'launchTemplate',
                launch_template_name="RenderingWithBatch",
                security_group=security_group,
                user_data=ec2.UserData.custom(user_data)
            )
            launch_template.node.add_dependency(security_group)

        return launch_template

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = self.__create_vpc()
        self.__create_launch_template(self.vpc)
