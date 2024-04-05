import aws_cdk as cdk

from stacks import PipelineStack, C9EnvStack


app = cdk.App()

PipelineStack(app, "RenderingWithBatch-Pipeline")
C9EnvStack(app, 'RenderingWithBatch-C9Environment')

app.synth()
