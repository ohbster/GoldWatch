#!/bin/bash

aws cloudformation deploy --stack-name gw-natgateway --template-file template.yaml
