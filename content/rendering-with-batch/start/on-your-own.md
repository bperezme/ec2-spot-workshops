---
title: "... On your own"
date: 2021-09-06T08:51:33Z
weight: 27
---

## Deploying the CloudFormation stack

As a first step, **download** the [starting CloudFormation stack](https://raw.githubusercontent.com/bpguasch/ec2-spot-workshops/blender_rendering_using_batch/content/rendering-with-batch/files/stack.yaml)
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

{{% notice warning %}}
Notice that in total there are two stacks that need to be fully deployed before moving forward; the one that you deployed and for which you chose a name,
and the one that is automatically deployed and is named **RenderingWithBatch-Pipeline**. Do not proceed with the workshop until you see both.
The deployment of both stacks will take roughly **6 minutes**.
{{% /notice %}}

{{% insert-md-from-file file="rendering-with-batch/start/review-outputs.md" %}}
