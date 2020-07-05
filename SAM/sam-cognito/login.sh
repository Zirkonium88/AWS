#!/bin/bash

USERPOOLID="eu-central-1_VkjGmlJDV"
CLIENT_ID="5tnu1koa4dhc8fp3u9090gknv9"
USERNAME="malte.walkowiak@gmx.de"
PASSWORD="Hsv+1896"
UNAUTH_ENDPOINT="https://esin9jp1uf.execute-api.eu-central-1.amazonaws.com/v1/unauth"
AUTH_ENDPOINT="https://esin9jp1uf.execute-api.eu-central-1.amazonaws.com/v1/unauth"

AUTH_TOKEN=$(aws cognito-idp initiate-auth \
--auth-flow USER_PASSWORD_AUTH \
--auth-parameters USERNAME=${USERNAME},PASSWORD=${PASSWORD} \
--client-id "${CLIENT_ID}" | jq -r .AuthenticationResult.AccessToken)
printf "\n"
echo "${AUTH_TOKEN}"
printf "\n"
echo "Let's call the unauthenticated endpoint ... "
curl "${UNAUTH_ENDPOINT}"
printf "\n"
printf "\n"
echo "And now, let's call the authenticated endpoint ... "
curl -H 'Authorization: "${AUTH_TOKEN}"' "${AUTH_ENDPOINT}"
