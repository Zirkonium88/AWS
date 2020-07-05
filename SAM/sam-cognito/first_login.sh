#!/bin/bash

USERPOOLID="eu-central-1_VkjGmlJDV"
CLIENT_ID="5tnu1koa4dhc8fp3u9090gknv9"
USERNAME="malte.walkowiak@gmx.de"
PASSWORD=$1

# Do an initial login
# It will come back wtih a challenge response
AUTH_CHALLENGE_SESSION=$(aws cognito-idp initiate-auth \
--auth-flow USER_PASSWORD_AUTH \
--auth-parameters USERNAME=${USERNAME},PASSWORD=${PASSWORD} \
--client-id "${CLIENT_ID}" | jq -r .Session)

# # Then respond to the challenge
AUTH_TOKEN=$(aws cognito-idp admin-respond-to-auth-challenge \
--user-pool-id "${USERPOOLID}" \
--client-id "${CLIENT_ID}" \
--challenge-responses "NEW_PASSWORD=Hsv+1896,USERNAME=${USERNAME}" \
--challenge-name NEW_PASSWORD_REQUIRED \
--session "${AUTH_CHALLENGE_SESSION}" | jq -r .AuthenticationResult.IdToken)

# Tell the world
printf "\n"
echo "Changed the password to Hsv+1896"
printf "\n"
echo "Logged in ID Auth Token: "
echo $AUTH_TOKEN
printf "\n"
