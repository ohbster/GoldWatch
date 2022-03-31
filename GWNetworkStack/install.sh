#!/bin/bash
aws cloudformation deploy --stack-name gw-network --template-file template.yaml; &

watch -n 5 -d aws cloudformation describe-stack-resources --stack-name gw-network --query 'StackResources[*].[ResourceType,ResourceStatus]' --output table;

