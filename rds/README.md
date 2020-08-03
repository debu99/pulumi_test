# RDS

### What Is This?

This is Pulumi code for deploying RDS in the private subnet on top of [previously configured vpc](../vpc). The RDS is able to access from API instances only.

### How To Use It?

We use AWS S3 backend for saving states.

&nbsp;  1-4. points you need to do only [once](../vpc).

5. Go inside this dir and create stack:
```
$ pulumi stack init rds
```

6. Create Python venv and install dependencies:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

7. Copy `Pulumi.template.yaml` data to automatically created `Pulumi.rds.yaml`:
```
$ cat Pulumi.template.yaml >> Pulumi.rds.yaml
```

8. Edit `Pulumi.rds.yaml` according to your needs and launch:
```
$ pulumi up
```

9. Destroy when you finished your experiments:
```
$ pulumi destroy
$ pulumi stack rm rds
```
