---
title: "Cleaning up"
date: 2021-09-06T08:51:33Z
weight: 70
---

Before closing this workshop, let's make sure we clean up all the resources we created so we do not incur any unexpected costs.

## AWS Batch

When deleting AWS Batch components, the order matters; a CE cannot be deleted if it is associated to a valid queue, so we have to start by deleting the queue. Job queues and compute environments have to be disabled bore deleting them.

To disable the components:

:::code{language="bash"}
aws batch update-job-queue --job-queue "${RENDERING_QUEUE_NAME}" --state DISABLED && \
aws batch update-compute-environment --compute-environment "${SPOT_COMPUTE_ENV_ARN}" --state DISABLED && \
aws batch update-compute-environment --compute-environment "${ONDEMAND_COMPUTE_ENV_ARN}" --state DISABLED
:::

To learn more about these APIs, see [update-job-queue CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/batch/update-job-queue.html) and [update-compute-environment CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/batch/update-compute-environment.html).

::::alert{type="info"}
The previous operation may take up to 2 minutes. Job queues and compute environments cannot be deleted while being modified, so running the commands below while the compute environments and job queue are being disabled might result in an error with the message "resource is being modified".
::::

To delete the components:

:::code{language="bash"}
aws batch delete-job-queue --job-queue "${RENDERING_QUEUE_NAME}"
aws batch delete-compute-environment --compute-environment "${SPOT_COMPUTE_ENV_ARN}"
aws batch delete-compute-environment --compute-environment "${ONDEMAND_COMPUTE_ENV_ARN}"
:::

To learn more about these APIs, see [delete-job-queue CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/batch/delete-job-queue.html) and [delete-compute-environment CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/batch/delete-compute-environment.html).

Finally, deregister the job definition:

:::code{language="bash"}
aws batch deregister-job-definition --job-definition "${JOB_DEFINITION_ARN}"
:::

To learn more about this API, see [deregister-job-definition CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/batch/deregister-job-definition.html).

## AWS FIS

To remove the AWS FIS template:

:::code{language="bash"}
aws fis delete-experiment-template --id ${FIS_TEMPLATE}
:::

To learn more about this API, see [delete-experiment-template CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/fis/delete-experiment-template.html).

## Deleting the CloudFormation stacks

Deleting a CloudFormation Stack will delete all the resources it created.
To do that, navigate to [CloudFormation in the AWS Console](https://console.aws.amazon.com/cloudformation/home),
select the stack **RenderingWithBatch-Pipeline** and delete it. Delete also the stack that you created at the beginning of the workshop.
