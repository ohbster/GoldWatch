#!/bin/bash

if [ -z $1 ]
then
	echo -e "Syntax error. No argument given. \nCorrect usage: test.sh <argument>"
else
	echo "Your argument was {$1}"
fi
