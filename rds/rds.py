import pulumi
import pulumi_aws as aws

# read local config settings
config = pulumi.Config()
rds_username = config.require("rds_username")
rds_password = config.require("rds_password")
vpc_stack = config.require("vpc_stack")
ec2_stack = config.require("ec2_stack")

# get stack reference from vpc and ec2
vpc = pulumi.StackReference(vpc_stack)
ec2 = pulumi.StackReference(ec2_stack)

# get vpc/subnet/securitygroup
vpc_id = vpc.get_output("vpc_id")
vpc_azs = vpc.get_output("vpc_azs")
private_subnets = vpc.get_output("private_subnets")
private_subnet_ids = vpc.get_output("private_subnet_ids")
api_sg_id = ec2.get_output("api_sg_id")

# create reds security group
rds_sg = aws.ec2.SecurityGroup(
    resource_name = "rds access - 3306",
    vpc_id=vpc_id,
    description="Enable RDS access",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 3306,
            "to_port": 3306,
            "security_groups": [api_sg_id],
        }
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"],}
    ],
)

# create rds subnet
db_subnet = aws.rds.SubnetGroup(
	resource_name = "db_subnet",
    subnet_ids = private_subnet_ids,
    tags={"Name": "DB subnet group"})

# creat rds instance
rds = aws.rds.Instance(
	resource_name = "rds",
	availability_zone = vpc_azs[0],
	db_subnet_group_name = db_subnet,
	vpc_security_group_ids = [rds_sg.id],
    storage_type = "gp2",
    multi_az = False,
    allocated_storage = 20,
    engine = "mysql",
    engine_version = "5.7",
    instance_class = "db.t2.micro",
    name = "test_rds",
    parameter_group_name = "default.mysql5.7",
    skip_final_snapshot = True,
    username = rds_username,
    password = rds_password,
    )