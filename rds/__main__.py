import pulumi

import rds

#export rds endpoint
pulumi.export('rds_address', rds.rds.address)
pulumi.export('rds_endpoint', rds.rds.endpoint)
pulumi.export('rds_arn', rds.rds.arn)