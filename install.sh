#!/bin/bash

DEFAULTVPCID=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query 'Vpcs[*].VpcId' --output text);

echo ${DEFAULTVPCID};

sam build;
sam deploy --no-confirm-changeset &


