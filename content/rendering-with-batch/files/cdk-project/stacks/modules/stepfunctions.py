from aws_cdk import (
    aws_stepfunctions as stepfunctions,
    aws_stepfunctions_tasks as stepfunctions_tasks,
    Duration,
    NestedStack,
)

from constructs import Construct


class StepFunctionsModule(NestedStack):
    def __create_state_machine(self, bucket, preprocessing_func):
        # Create the rendering task
        rendering_task = stepfunctions_tasks.BatchSubmitJob(
            self, 'Rendering',
            job_name='$.Payload.body.jobName',
            job_queue_arn='$.Payload.body.jobQueueArn',
            job_definition_arn='$.Payload.body.jobDefinitionArn'
        )

        # Create the preprocessing (initial) task
        preprocessing_task = stepfunctions_tasks.LambdaInvoke(
            self, 'Number of frames extraction',
            lambda_function=preprocessing_func,
            task_timeout=stepfunctions.Timeout.duration(Duration.minutes(5))
        )
        preprocessing_task.next(rendering_task)

        # Create the state machine
        return stepfunctions.StateMachine(
            self, 'RenderingPipeline',
            definition_body=stepfunctions.DefinitionBody.from_chainable(preprocessing_task),
            timeout=Duration.days(1)
        )

    def __init__(self, scope: Construct, construct_id: str, bucket, preprocessing_func, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.state_machine = self.__create_state_machine(bucket, preprocessing_func)
