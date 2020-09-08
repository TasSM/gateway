# dpeloy

A dockerized nginx deployment automation for your CICD pipeline.

## Environment Variables
`HOSTED_ZONE_ID` = ID of the hosted zone in Route53 to add the DNS record
`RECORD_NAME` = DNS record name (e.g. server.bigcorp.com)
`DNS_TARGET` = ipv4 address or an existing domain (Will automatically create the appropriate A or CNAME record)

TODO:

0. Custom error pages + review base nginx.conf
2. Jenkinsfile