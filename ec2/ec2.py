import pulumi
import pulumi_aws as aws
import pulumi_random as random

# read local config settings
config = pulumi.Config()
certificate_arn = config.require("certificate_arn")
web_type = config.require("web_type")
api_type = config.require("api_type")
web_port = config.require_int("web_port")
api_port = config.require_int("api_port")
alb_port = config.require_int("alb_port")
vpc_stack = config.require("vpc_stack")

# get stack reference from vpc
vpc = pulumi.StackReference(vpc_stack)

# get vpc/subnet
vpc_id = vpc.get_output("vpc_id")
private_subnets = vpc.get_output("private_subnets")
private_subnet_ids = vpc.get_output("private_subnet_ids")
public_subnets = vpc.get_output("public_subnets")
public_subnet_ids = vpc.get_output("public_subnet_ids")

# get user data script for web
with open('web_user_data.tpl', 'r') as tpl_file:
    web_user_data = tpl_file.read()

# get user data script for api
with open('api_user_data.tpl', 'r') as tpl_file:
    api_user_data = tpl_file.read()

# get ssh public key
with open('key.pub', 'r') as key_file:
    public_key = key_file.read()

# upload ssh public key
key_name = "ssh_key_pair"
ssh_key_pair = aws.ec2.KeyPair(resource_name = "ssh_key_pair", key_name = key_name, public_key = public_key.rstrip('\n'))

# search ubuntu ami 
ubuntu_ami = aws.get_ami(
    filters=[
        {
            "name": "name",
            "values": ["ubuntu/images/hvm-ssd/ubuntu-*-18.04-amd64-server-*"],
        },
        {
            "name": "virtualization-type",
            "values": ["hvm"],
        },
    ],
    most_recent=True,
    owners=["099720109477"]
    )

# create bastion security group
bastion_sg = aws.ec2.SecurityGroup(
    resource_name = "bastion access - 22",
    vpc_id=vpc_id,
    description="Enable Bastion access",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": ["0.0.0.0/0"],
        }
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"],}
    ],
)

# create bastion
bastion = aws.ec2.Instance(
    resource_name = 'bastion',
    ami = ubuntu_ami.id,
    instance_type = "t2.micro",
    key_name = key_name,
    subnet_id = public_subnet_ids[0],
    vpc_security_group_ids=[bastion_sg.id],
    tags = {"Name": "bastion"},
)

# create alb security group
alb_sg = aws.ec2.SecurityGroup(
    resource_name = "alb access - {}".format(alb_port),
    vpc_id=vpc_id,
    description="Enable ALB access",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": alb_port,
            "to_port": alb_port,
            "cidr_blocks": ["0.0.0.0/0"],
        }
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"],}
    ],
)

# create web security group, only allow request from alb
web_sg = aws.ec2.SecurityGroup(
    resource_name = "web access - {}".format(web_port),
    vpc_id=vpc_id,
    description="Enable ALB access",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": web_port,
            "to_port": web_port,
            "security_groups": [alb_sg.id],
        }
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"],}
    ],
)

# create web instance
web_private_subnet_id = random.RandomShuffle(
    resource_name = "web_private_subnet_id",
    inputs = private_subnet_ids,
    result_count = 1)
web = aws.ec2.Instance(
    resource_name = 'web',
    ami = ubuntu_ami.id,
    instance_type = web_type,
    key_name = key_name,
    subnet_id = web_private_subnet_id.results[0],
    vpc_security_group_ids=[web_sg.id],
    user_data=web_user_data,
    tags = {"Name": "web"},
)

# create api security group, only allow request from alb
api_sg = aws.ec2.SecurityGroup(
    resource_name = "api access - {}".format(api_port),
    vpc_id=vpc_id,
    description="Enable ALB access",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": api_port,
            "to_port": api_port,
            "security_groups": [alb_sg.id],
        }
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"],}
    ],
)

# create api instance  
api_private_subnet_id = random.RandomShuffle(
    resource_name = "api_private_subnet_id",
    inputs = private_subnet_ids,
    result_count = 1)
api = aws.ec2.Instance(
    resource_name = 'api',
    ami = ubuntu_ami.id,
    instance_type = api_type,
    key_name = key_name,
    subnet_id = api_private_subnet_id.results[0],
    vpc_security_group_ids=[api_sg.id],
    user_data=api_user_data,
    tags = {"Name": "api"},
)


# create application loadbalancer
alb = aws.lb.LoadBalancer(
    resource_name = "alb",   
    load_balancer_type = "application",
    internal = False,
    security_groups = [alb_sg.id],
    subnets = public_subnet_ids,
    )

# create web target group
web_tg = aws.lb.TargetGroup(
    resource_name = "web-tg", 
    port = web_port, 
    protocol = "HTTP", 
    target_type = "instance", 
    vpc_id = vpc_id,
)

# register web instance into target group
web_target_group_attachment = aws.lb.TargetGroupAttachment(
    resource_name = "web_target_group_attachment",
    port = web_port,
    target_group_arn=web_tg.arn,
    target_id = web.id)

# create api target group
api_tg = aws.lb.TargetGroup(
    resource_name = "api-tg", 
    port = api_port, 
    protocol = "HTTP", 
    target_type = "instance", 
    vpc_id = vpc_id,
)

# register api instance into target group
api_target_group_attachment = aws.lb.TargetGroupAttachment(
    resource_name = "api_target_group_attachment",
    port = api_port,
    target_group_arn=api_tg.arn,
    target_id = api.id)


# create alb https listener
lb_listener = aws.lb.Listener(
    resource_name = "lb_listener",
    load_balancer_arn = alb.arn,
    port = 80,
    #port = 443,
    #certificate_arn = certificate_arn,
    #protocol = "HTTPS",
    #ssl_policy = "ELBSecurityPolicy-2016-08",
    default_actions = [{"type": "forward", "target_group_arn": web_tg.arn}],
)

# create alb listener rules
api_rule = aws.lb.ListenerRule(
    resource_name = "api_rule",
    actions=[{
        "target_group_arn": api_tg.arn,
        "type": "forward",
    }],
    conditions=[
        {
            "pathPattern": {
                "values": ["/api/*"],
            },
        },
        {
            "hostHeader": {
                "values": ["app.com"],
            },
        },
    ],
    listener_arn = lb_listener.arn,
    priority=100
    )
