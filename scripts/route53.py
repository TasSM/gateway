import boto3
from botocore.exceptions import ClientError
import json

class R53DomainManager:
    
    def __init__(self, hostedZone, **kwargs):
        self.hostedZone = hostedZone
        self.client = boto3.client("route53")
        if "debug" in kwargs and kwargs.get("debug") is True:
            self.debug = True
        else:
            self.debug = False

    def __debug(self, response):
        if self.debug is True:
            print(json.dumps(response, indent=4))

    def resolve_record(self, recordName):
        try:
            response = self.client.test_dns_answer(
                HostedZoneId=self.hostedZone,
                RecordName=recordName,
                RecordType='A'
            )
            self.__debug(response)
        except ClientError as err:
            print("Function {0} Encountered Exception: {1}".format("resolve_record",err))

    def create_Arecord(self, recordName, ip, **kwargs):
        try:
            response = self.client.change_resource_record_sets()
            self.__debug(response)
        except ClientError as err:
            print("Function {0} Encountered Exception: {1}".format("resolve_record",err))


domain_mgr = R53DomainManager('Z03233031BTY3TL4UAL96', debug=True)

domain_mgr.resolve_record('test.devprod1.com')