# EC2

### What Is This?

This is Pulumi code for deploying EC2 instances on top of [previously configured vpc](../vpc). Bastion instance is located in the public subnet allow SSH access from anywhere, Web and API instances are located in the private subnet and are able to access from AWS ALB.

### How To Use It?

We use AWS S3 backend for saving states.

&nbsp;  1-4. points you need to do only [once](../vpc).

5. Go inside this dir and create stack:
```
$ pulumi stack init ec2
```

6. Create Python venv and install dependencies:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

7. Copy `Pulumi.template.yaml` data to automatically created `Pulumi.ec2.yaml`:
```
$ cat Pulumi.template.yaml >> Pulumi.ec2.yaml
```

8. Edit `Pulumi.ec2.yaml` according to your needs and launch:
```
$ pulumi up
```

9. Destroy when you finished your experiments:
```
$ pulumi destroy
$ pulumi stack rm ec2
```
