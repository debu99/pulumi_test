import unittest
import pulumi

class MyMocks(pulumi.runtime.Mocks):
    def new_resource(self, type_, name, inputs, provider, id_):
        return [name + '_id', inputs]
    def call(self, token, args, provider):
        return {}

pulumi.runtime.set_mocks(MyMocks())

import infra

config = pulumi.Config()
vpc_name = config.require("vpc_name")
vpc_cidr = config.require("vpc_cidr")
private_subnets = config.require_object("private_subnets")
public_subnets = config.require_object("public_subnets")
zones = config.require_int("zones")


class TestingWithMocks(unittest.TestCase):

    @pulumi.runtime.test
    def test_vpc(self):
        def check_vpc(args):
            urn, tags = tags
            self.assertTrue(tags['Name'] == vpc_name, f'vpc {vpc_name} exists')

        return pulumi.Output.all(vpc.vpc.urn, vpc.vpc.tags).apply(check_vpc)
