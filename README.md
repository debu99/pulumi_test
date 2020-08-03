# Pulumi Test

### What Is This?

This is Pulumi code for deploying EC2/RDS/Elasticache instances on top of [ configured vpc](./vpc). Bastion instance is located in the public subnet and allowing SSH access from anywhere, Web and API instances are located in the private subnet and are able to access from AWS ALB.

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

* Go to vpc, ec2, elasticache, rds folders and repeate step 5-8  

5. Go to each folder(vpc->ec2->elasticache->rds) and create stack:
```
$ pulumi stack init `echo $PWD | awk -F'/' '{print $NF}'`
```

6. Create Python venv and install dependencies:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

7. Copy `Pulumi.template.yaml` data to automatically created `Pulumi.{DIRECTORY_NAME}.yaml`:
```
$ cat Pulumi.template.yaml >> Pulumi.`echo $PWD | awk -F'/' '{print $NF}'`.yaml
```

8. Edit `Pulumi.{DIRECTORY_NAME}.yaml` according to your needs and launch:
```
$ pulumi up
```

9. Go to folder(rds->elasticache->ec2->vpc) and destroy if you finished your experiments:
```
$ pulumi destroy
$ pulumi stack rm `echo $PWD | awk -F'/' '{print $NF}'`
```
