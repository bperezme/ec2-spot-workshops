---
title: "On your own"
weight: 22
---

As a first step, download the [starting CloudFormation stack](https://raw.githubusercontent.com/bpguasch/ec2-spot-workshops/blender_rendering_using_batch/content/rendering-with-batch/assets/starting_stack.yaml)
that will deploy for you a Cloud9 environment. This environment will automatically download and deploy a [CDK project](https://aws.amazon.com/cdk/) with the
following resources to implement the rendering pipeline:

- A VPC
- An S3 bucket
- An ECR repository
- A Launch Template
- An AWS Step Functions state machine
- An instance profile for AWS Batch compute environment
- An AWS IAM Role used by AWS Fault Injection Simulator

After downloading the template, open the [CloudFormation console](https://console.aws.amazon.com/cloudformation) and on the top-right corner of the screen, click on **Create stack**. Then, follow these steps:

1. In the **Create stack** page, click on **Choose file** and upload the CloudFormation template you just downloaded. Don't change any other configuration parameter.
2. In the **Specify stack details** page, set a stack name.
3. In the **Configure stack options** page, leave all the configuration as it is. Navigate to the bottom of the page and click on **Next**.
4. In the **Review** page, leave all the configuration as it is. Navigate to the bottom of the page, and click on **I acknowledge that AWS CloudFormation might create IAM resources** and finally on **Create stack**.

::::alert{type="warning"}
Notice that in total there are two stacks that need to be fully deployed before moving forward; the one that you deployed and for which you chose a name,
and the one that is automatically deployed and is named **RenderingWithBatch-Pipeline**. Do not execute any commands until you see both.
The deployment of both stacks will take roughly **6 minutes**. In the meantime, you can explore the [Rendering pipeline](/rendering_pipeline)
::::

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