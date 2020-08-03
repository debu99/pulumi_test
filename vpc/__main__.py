import pulumi

import vpc

pulumi.export("vpc_name", vpc.vpc_name)
pulumi.export("private_subnets", vpc.private_subnets)
pulumi.export("public_subnets", vpc.public_subnets)
pulumi.export("vpc_id", vpc.vpc.id)
pulumi.export("vpc_azs", vpc.vpc_azs)
pulumi.export("public_subnet_ids", vpc.public_subnet_ids)
pulumi.export("private_subnet_ids", vpc.private_subnet_ids)


