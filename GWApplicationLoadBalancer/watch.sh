#!/bin/bash

watch -n 5 -d aws cloudformation describe-stack-resources --stack-name gw-alb --query 'StackResources[*].[ResourceType,ResourceStatus]' --output table;

