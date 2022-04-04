#!/bin/bash
#!/bin/bash

if [ -z "$1" ]
then
	echo -e "\nPlease provide a Name for an existing EC2 KeyPair for SSH access to EC2 Instance"
	echo -e "\nCorrect usage: ./install <KeyPair Name>"
else

    sam build;
    sam deploy --parameter-overrides KeyName=\""$1"\" --no-confirm-changeset

fi

