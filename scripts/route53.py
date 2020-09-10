import boto3
from botocore.exceptions import ClientError
import json
import datetime

class Route53DomainManager:

    def __init__(self, hosted_zone, **kwargs):
        self.hosted_zone = hosted_zone
        self.client = boto3.client("route53")
        if "debug" in kwargs and kwargs.get("debug") is True:
            self.debug = True
        else:
            self.debug = False

    def __debug(self, response):
        if self.debug is True:
            print(json.dumps(response["ResponseMetadata"], indent=4))

    def test_record(self, record_type, record_name):
        try:
            response = self.client.test_dns_answer(
                HostedZoneId=self.hosted_zone,
                RecordName=record_name,
                RecordType=record_type
            )
            self.__debug(response)
            return response["RecordData"]
        except ClientError as err:
            print("Function {0} Encountered Exception: {1}".format("test_record",err))
            exit(1)

    def create_record(self, record_type, record_name, target, **kwargs):
        try:
            if "ttl" in kwargs and isinstance(kwargs.get("ttl"), int):
                ttlValue = max(60, min(kwargs.get("ttl"), 172800))
            else:
                ttlValue = 300  
            timestamp = datetime.datetime.now().strftime("%M-%D-%YT%H:%M:%S")
            response = self.client.change_resource_record_sets(
                HostedZoneId=self.hosted_zone,
                ChangeBatch={
                    "Comment": "Modified by Route53DomainManager at {0}".format(timestamp),
                    "Changes": [
                        {
                            "Action": "CREATE",
                            "ResourceRecordSet": {
                                "Name": record_name,
                                "Type": record_type,
                                "TTL": ttlValue,
                                "ResourceRecords": [
                                    {
                                        "Value": target
                                    }
                                ]
                            }
                        }
                    ]
                }
            )
            self.__debug(response)
        except ClientError as err:
            print("Function {0} Encountered Exception: {1}".format("create_record",err))
            exit(1)

