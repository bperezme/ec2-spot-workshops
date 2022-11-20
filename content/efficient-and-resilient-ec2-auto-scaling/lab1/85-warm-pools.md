---
title: "Scaling your application faster"
menuTitle: "Warm pools"
weight: 182

---

## Warm Pools

A warm pool is a pool of pre-initialized EC2 instances that sits alongside an Auto Scaling group. Whenever your application needs to scale out, gives you the ability to decrease latency for your applications that have exceptionally long boot times.

**Three options to set the warm pool size:**

It's important to decide how to set the warm pools size as it will make huge difference in associated cost.

1. By default warm pool size is the difference between the number of currently running instances and the maximum capacity.
2. However if you're running a large Auto Scaling group that won't be the best cost optimized option, in that case you can set a maximum prepared capacity which counts current running instances as part of it.
3. Or you can also set a static number as the minimum pool size.

You can keep instances in the warm pool in one of **three** states: **Stopped**, **Running**, or **Hibernated**.
Keeping instances in a **Stopped** state is an effective way to **minimize costs**. With stopped instances, you pay only for the volumes that you use and the Elastic IP addresses attached to the instances.

Lifecycle hooks can be used to put instances in wait state before launch or terminate.

**Reusing instances**, by default when ASG scales in instances it get terminates but you can configure reuse policy to return instances to warm pool. only available in CLI and CDK.


{{% notice info %}}
**Limitations**:
You cannot add a warm pool to Auto Scaling groups that have a mixed instances policy or that launch Spot Instances.
{{% /notice %}}

![predictive-scaling](/images/efficient-and-resilient-ec2-auto-scaling/warm-pools-lifecycle-diagram.png)

#### Enable Warm Pools for the Auto Scaling Group

Let's add a Warm Pool to our Auto Scaling group so we can pre-initialize our instances so that they can be brought into service more rapidly.

#### Add a Warm Pool

We will keep our Warm Pool instances in a stopped state after they have completed their initialization actions. We will set the optional Warm Pool sizing parameters `--min-size` to 2 and leave `--max-group-prepared-capacity` empty. This means that this Warm Pool will have a minimum size of 2 and a maximum prepared capacity equal to the max size of the Auto Scaling group.
The maximum prepared capacity will include instances launched into the Auto Scaling group, and instances launched into the Warm Pool.

```bash
aws autoscaling put-warm-pool --auto-scaling-group-name "ec2-workshop-asg" --pool-state Stopped --min-size 2
```