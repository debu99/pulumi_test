# VPC

### What Is This?

This is Pulumi code for deploying AWS VPC with 4 subnets (2 public and 2 private) in 2 AZs. Each private subnet needs NAT gateway/EIP for Internet access.

### How To Use It?

We use AWS S3 backend for saving states.

1. Install Pulumi https://www.pulumi.com/docs/get-started/install/.

2. Create a bucket in web console or with command:
```
$ aws s3api create-bucket --bucket test-states-bucket --region ap-southeast-1

$ aws s3api put-bucket-versioning --bucket test-states-bucket
```

3. Export AWS variables:
```
$ export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXX
$ export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXX
$ export AWS_REGION=ap-southeast-1
```
For more information, please refer to https://www.pulumi.com/docs/intro/cloud-providers/aws/setup/.

4. Login with Pulumi to s3:
```
$ pulumi login s3://test-states-bucket
```

5. Go inside this dir and create stack:
```
$ pulumi stack init vpc
```

6. Create Python venv and install dependencies:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

7. Copy `Pulumi.template.yaml` data to automatically created `Pulumi.vpc.yaml`:
```
$ cat Pulumi.template.yaml > Pulumi.vpc.yaml
```

8. Edit `Pulumi.vpc.yaml` according to your needs and launch:
```
$ pulumi up
```

9. Destroy when you finished your experiments:
```
$ pulumi destroy
$ pulumi stack rm vpc
``` 