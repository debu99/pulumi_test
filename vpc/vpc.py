import pulumi
import pulumi_aws as aws

# read local config settings
config = pulumi.Config()
vpc_name = config.require("vpc_name")
vpc_cidr = config.require("vpc_cidr")
private_subnets = config.require_object("private_subnets")
public_subnets = config.require_object("public_subnets")
zones = config.require_int("zones")

# get availability zones
aws_availability_zones = aws.get_availability_zones(state="available")

# create vpc
vpc = aws.ec2.Vpc(
    resource_name = vpc_name,
    assign_generated_ipv6_cidr_block = False,
    cidr_block = vpc_cidr,
    enable_dns_hostnames = True,
    enable_dns_support = True,
    tags = {"Name": vpc_name},
    )

# create internet gateway
igw = aws.ec2.InternetGateway("{}-igw".format(vpc_name), vpc_id=vpc.id)

# create public subnet routing table
public_rt = aws.ec2.RouteTable(
    resource_name ="{}-public-rt".format(vpc_name),
    vpc_id = vpc.id,
    routes = [{"cidr_block": "0.0.0.0/0", "gateway_id": igw.id}],
    tags = {"Name":  "-public-rt".format(vpc_name)},
)

public_subnet_ids = []
private_subnet_ids = []
vpc_azs = []

# create public subnet and associate to public routing table based on the subnet number 
for index, (zone, public_subnet) in enumerate(zip(aws_availability_zones.names, public_subnets)):
    vpc_azs.append(zone)

    public_subnet = aws.ec2.Subnet(
        resource_name = "{}-public-subnet-{}".format(vpc_name, index),
        assign_ipv6_address_on_creation = False,
        vpc_id = vpc.id,
        map_public_ip_on_launch = True,
        cidr_block = public_subnet,
        availability_zone=zone,
        tags={"Name": "{}-public-subnet-{}".format(vpc_name, index)},
    )
    aws.ec2.RouteTableAssociation(
        resource_name = "{}-public-rta-{}".format(vpc_name, index),
        route_table_id = public_rt.id,
        subnet_id = public_subnet.id,
    )
    public_subnet_ids.append(public_subnet.id)


# create private subnet, natgateway, private routing table and associate private subnet to its routing table based on the subnet number
for index, (zone, private_subnet) in enumerate(zip(aws_availability_zones.names, private_subnets)):
    private_subnet = aws.ec2.Subnet(
        resource_name = "{}-private-subnet-{}".format(vpc_name, index),
        assign_ipv6_address_on_creation = False,
        vpc_id = vpc.id,
        map_public_ip_on_launch = False,
        cidr_block = private_subnet,
        availability_zone = zone,
        tags={"Name": "{}-private-subnet-{}".format(vpc_name, index)},
    )
    eip = aws.ec2.Eip("{}-eip-natgw-{}".format(vpc_name, index), tags={"Name": "{}-eip-natgw-{}".format(vpc_name, index)})
    nat_gateway = aws.ec2.NatGateway(
        resource_name = "{}-natgw-{}".format(vpc_name, index),
        subnet_id = public_subnet.id,
        allocation_id = eip.id,
        tags = {"Name": "{}-natgw-{}".format(vpc_name, index)},
    )
    private_rt = aws.ec2.RouteTable(
        resource_name = "{}-private-rt-{}".format(vpc_name, index),
        vpc_id = vpc.id,
        routes = [{"cidr_block": "0.0.0.0/0", "gateway_id": nat_gateway.id}],
        tags = {"Name": "{}-private-rt-{}".format(vpc_name, index)},
    )
    aws.ec2.RouteTableAssociation(
        resource_name = "{}-private-rta-{}".format(vpc_name, index),
        route_table_id = private_rt.id,
        subnet_id = private_subnet.id,
    )
    private_subnet_ids.append(private_subnet.id)
