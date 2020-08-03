import pulumi

import elasticache

# export redis endpoint
pulumi.export('redis_primary_endpoint_address', elasticache.redis.primary_endpoint_address)
pulumi.export('redis_configuration_endpoint_address', elasticache.redis.configuration_endpoint_address)