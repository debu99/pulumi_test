import pulumi
import pulumi_aws as aws

# read local config settings
config = pulumi.Config()
node_type = config.require("node_type")
node_port = config.require("node_port")
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

# create redis security group
redis_sg = aws.ec2.SecurityGroup(
    resource_name = "redis access - {}".format(node_port),
    vpc_id=vpc_id,
    description="Enable Redis access",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": node_port,
            "to_port": node_port,
            "security_groups": [api_sg_id],
        }
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"],}
    ],
)

# create redis subnet
redis_subnet = aws.elasticache.SubnetGroup(
	resource_name = "redis_subnet", 
	name = "redis-subnet",
	subnet_ids = private_subnet_ids,
	)

# create redis replication group
redis = aws.elasticache.ReplicationGroup(
	resource_name = "redis",
	engine = "redis",
    automatic_failover_enabled = False,
    #availability_zones = vpc_azs,
    node_type = node_type,
    number_cache_clusters = 1,
    parameter_group_name="default.redis5.0",
    security_group_ids = [redis_sg.id],
    port = node_port,
    subnet_group_name = redis_subnet.id,
    replication_group_description="test description")