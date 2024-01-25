# import necessary libraries for handling HTTP requests, working with JSON

from flask import Flask, jsonify, request
from flask_oauthlib.provider import OAuth2Provider 

import sys
import requests
import json
import logging
import time

# capturing SSL/TLS-related warnings.

logging.captureWarnings(True)

# base URL

test_api_url = "https://mywebsite.com"

# function to obtain a new OAuth 2.0 token from the authentication server

def get_new_token():

auth_server_url = "https://mywebsite.com/authz-service/oauth/token"
client_id = 'customer_id'
client_secret = 'customer_pass'

token_req_payload = {'grant_type': 'client_credentials'}

token_response = requests.post(auth_server_url, data=token_req_payload, verify=False, allow_redirects=False, auth=(client_id, client_secret))
			 
if token_response.status_code !=200:
			print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
			sys.exit(1)

			print("Successfuly obtained a new token")
			tokens = json.loads(token_response.text)
			return tokens['access_token']


# obtain a token before calling the API

token = get_new_token()

# call the API with token

while True:

    api_call_headers = {'Authorization': 'Bearer ' + token}
    api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)

# token refresh

if	api_call_response.status_code == 401:
    token = get_new_token()
else:
    print(api_call_response.text)

time.sleep(60)