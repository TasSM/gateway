# gateway

A dockerized nginx deployment automation for your CICD pipeline.

## Environment Variables

### MANDATORY

`GATEWAY_FQDN` = DNS record name (e.g. server.bigcorp.com)

`GATEWAY_HOST` = ipv4 address or an existing domain (Will automatically create the appropriate A or CNAME record)

`GATEWAY_USER` = SSH user for the webserver

`CERTBOT_EMAIL` = E-mail address to register TLS certificate against


### REQUIRED FOR Route53 RECORD CREATION

`HOSTED_ZONE_ID` = ID of the hosted zone in Route53 to add the DNS record

`AWS_ACCESS_KEY_ID` = AWS Access Key ID

`AWS_SECRET_ACCESS_KEY` = AWS secret access key

## Volumes

Mount the Gateway SSH key as volume: `/root/.ssh/gw-key` 


## Docker Commands
```
docker build -t gateway:prod .
```

```
docker run -v $(pwd)/ssh_key:/root/.ssh/gw-key  ...-e ENVIRONMENT VARIABLES... gateway:prod
```

#### TODO

1. Teardown scripts (revoke certs)
2. Jenkinsfile
3. custom entry points
4. customer error pages