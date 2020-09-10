import route53
import os
import time
import re

def main(hosted_zone, record_name, target,):
    r53 = route53.Route53DomainManager(hosted_zone, debug=True)
    record_type = "A"
    if re.search('[a-zA-Z]', target):
        record_type = "CNAME"
    r53.create_record(record_type, record_name, target)

if __name__=="__main__":
    zone_id = os.environ["HOSTED_ZONE_ID"]
    record_name = os.environ["GATEWAY_FQDN"]
    target = os.environ["GATEWAY_HOST"]
    main(zone_id, record_name, target)