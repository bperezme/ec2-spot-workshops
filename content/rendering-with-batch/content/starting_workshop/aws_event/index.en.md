---
title: "At an AWS guided event"
weight: 21
---

This workshop creates an AWS account and several resources for you. You will need the Participant Hash provided at your AWS hosted workshop, and your email address to track your unique session.

Once you've reviewed the T&Cs and joined the event, you will be taken to the AWS workshop studio home page where you can access the console and workshop instructions. You can access the console of your provisioned AWS account for the event by clicking the link in the sidebar:

![Access account](/static/access_account.png)

You are now logged in to the AWS console in an account that was created for you, and will be available only throughout the workshop run time. A CloudFormation stack has been automatically deployed for you with the following resources:

- A VPC
- An S3 bucket
- An ECR repository
- A Launch Template
- An AWS Step Functions state machine
- An instance profile for AWS Batch compute environment
- The Cloud9 environment where you will run all the commands
- An AWS IAM Role used by AWS Fault Injection Simulator

## Reviewing the Launch Template

Note that the `UserData` of the created Launch Template contains the following script:

```
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="==MYBOUNDARY=="

--==MYBOUNDARY==
Content-Type: text/x-shellscript; charset="us-ascii"

#!/bin/bash
echo "ECS_ENABLE_SPOT_INSTANCE_DRAINING=true" >> /etc/ecs/ecs.config
echo "ECS_CONTAINER_STOP_TIMEOUT=90s" >> /etc/ecs/ecs.config
echo "ECS_ENABLE_CONTAINER_METADATA=true" >> /etc/ecs/ecs.config

--==MYBOUNDARY==--
```

What we are doing here is enabling [Spot Instance Draining](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html). When ECS Spot Instance draining is enabled on the instance, ECS receives the Spot Instance interruption notice and places the instance in DRAINING status. When a container instance is set to DRAINING, Amazon ECS prevents new tasks from being scheduled for placement on the container instance. To learn more about Spot instance interruption notices, visit [Spot Instance interruption notices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-interruptions.html#spot-instance-termination-notices).

## Gathering the CloudFormation outputs
You will create other AWS resources using the AWS CLI in [Cloud9](https://aws.amazon.com/cloud9/), a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a browser. It includes a code editor, debugger, and terminal. Cloud9 comes prepackaged with essential tools for popular programming languages, including JavaScript, Python, PHP, and more.

Navigate to the [Cloud9 console](https://console.aws.amazon.com/cloud9) and open the environment that was created for you. Execute the following commands to retrieve the outputs of the CloudFormation stack:

:::code{language="bash"}
token=$(curl -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-ec2-metadata-token-ttl-seconds:21600')
export AWS_DEFAULT_REGION=$(curl -H "X-aws-ec2-metadata-token:$token" http://169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
export STACK_NAME="RenderingWithBatch-Pipeline"

for output in $(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query 'Stacks[].Outputs[].OutputKey' --output text)
do
    export $output=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query 'Stacks[].Outputs[?OutputKey==`'$output'`].OutputValue' --output text)
    eval "echo $output : \"\$$output\""
done
:::

You can now start the workshop by heading to [**Rendering pipeline**](/rendering_pipeline).