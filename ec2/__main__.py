import pulumi

import ec2

pulumi.export('alb_dns_name', ec2.alb.dns_name)
pulumi.export('bastion_public_ip', ec2.bastion.public_ip)
pulumi.export('web_private_ip', ec2.web.private_ip)
pulumi.export('api_private_ip', ec2.api.private_ip)
pulumi.export('api_sg_id', ec2.api_sg.id)
pulumi.export('api_sg_name', ec2.api_sg.name)


