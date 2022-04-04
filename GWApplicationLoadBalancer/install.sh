#!/bin/bash

if [ -z $1 ]
then
	echo -e "\nPlease provide a Certificate ARN for Application Load Balancer"
	echo -e "\nCorrect usage: ./install <AcmCertificate>"
else
	aws cloudformation deploy --stack-name gw-alb --template template.yaml \
	--parameter-overrides AcmCertificate=$1

	#--parameter-overrides file://parameter-overrides.json & \

fi
