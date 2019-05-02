#!/bin/bash
# Deploy content for my trainings
# 
# Use the credential helper to avoid passing usernam and password every time
# git config credential.helper store
# git push https://git-codecommit.eu-central-1.amazonaws.com/v1/repos/trc-trainings-hp
#
# run deploy.sh with "sh deploy.sh"
# Use the first argument to insert the commit message

git add .
git commit -m "$1"
echo $1
git push

