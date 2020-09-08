import route53
import os
import time

def main(hosted_zone, record_name, target,):
    r53 = route53.Route53DomainManager(hosted_zone, debug=True)
    record_type = "A"
    for seg in record_name.split("."):
        if not seg.isnumeric():
            record_type = "CNAME"
            break
    r53.create_record(record_type, record_name, target)

if __name__=="__main__":
    zone_id = os.environ["HOSTED_ZONE_ID"]
    record_name = os.environ["RECORD_NAME"]
    target = os.environ["DNS_TARGET"]
    main(zone_id, record_name, target)