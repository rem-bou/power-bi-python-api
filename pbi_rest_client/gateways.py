#!/usr/bin/env python

import logging
import requests
import os

from typing import List
from string import Template
from .helpers.serializecredentials import Helpers
from .helpers.asymmetrickeyencryptor import AsymmetricKeyEncryptor

class Gateways:
    def __init__(self, client):
        self.client = client
        self.helpers = Helpers()
        self.gateway = {}
        self.gateway_parameters = {}
        self.gateway_json = {}
        self.gateways = None
        self.datasource = None
        self.datasources = {}
        self.datasource_json = {}
        self.datasources_users = {}
        self.user_json = {}
        self.server_name = None
        self.database_name = None
        self.connection_details = None
        self.credential_details = None
        self.encrypted_credentials = None

    def payload_string_builder(self, credential_type: str) -> str:
        self.server_name = os.getenv('AZURE_SERVER_NAME')
        self.database_name = os.getenv('AZURE_DB_NAME')
        datasource_username = os.getenv('DATASOURCE_USERNAME')
        datasource_password = os.getenv('DATASOURCE_PASSWORD')
        credential_array = [datasource_username, datasource_password]

        connection_details = Template("{\"server\":\"$server_name\",\"database\":\"$database_name\"}")
        self.connection_details = connection_details.substitute(server_name=self.server_name, database_name=self.database_name)
        
        credential_details = self.helpers.serialize_credentials(credential_array, credential_type)

        public_key = {
            'exponent': self.gateway['publicKey']['exponent'],
            'modulus': self.gateway['publicKey']['modulus']
        }

        key_encryptor = AsymmetricKeyEncryptor(public_key)
        self.encrypted_credentials = key_encryptor.encode_credentials(credential_details)

        return self.connection_details, self.encrypted_credentials

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-gateways
    def get_gateways(self) -> List:
        self.client.check_token_expiration()

        url = self.client.base_url + "gateways"
        
        response = requests.get(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info("Successfully retrieved gateways.")
            self.gateways = response.json()["value"]
            return self.gateways
        else:
            logging.error("Failed to retrieve gateways.")
            self.client.force_raise_http_error(response)

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-gateway
    def get_gateway(self, gateway_name: str) -> List:
        self.client.check_token_expiration()
        self.get_gateways()
        gateway_found = False

        for item in self.gateways: 
            if item["name"] == gateway_name: 
                logging.info("Found gateway with name " + gateway_name)
                gateway_found = True
                self.gateway_json = item
                break

        if gateway_found == False:
            logging.warning("Unable to find gateway with name: " + gateway_name)
            return

        url = self.client.base_url + "gateways/" + self.gateway_json['id']
        
        response = requests.get(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info("Successfully retrieved gateway with name: " + gateway_name)
            self.gateway = response.json()
            return self.gateway
        else:
            logging.error("Failed to retrieve gateway with name: " + gateway_name)
            self.client.force_raise_http_error(response)

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-datasources
    def get_datasources(self, gateway_name: str) -> List:
        self.client.check_token_expiration()
        self.get_gateway(gateway_name)

        url = self.client.base_url + "gateways/" + self.gateway['id'] + "/datasources"
        
        response = requests.get(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info("Successfully retrieved datasources.")
            self.datasources = response.json()["value"]
            return self.datasources
        else:
            logging.error("Failed to retrieve datasources.")
            self.client.force_raise_http_error(response)

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-datasource
    def get_datasource(self, gateway_name: str, datasource_name: str) -> List:
        self.client.check_token_expiration()
        self.get_datasources(gateway_name)
        datasource_found = False

        for item in self.datasources: 
            if item["datasourceName"] == datasource_name: 
                logging.info("Found datasource with name: " + datasource_name)
                datasource_found = True
                self.datasource_json = item
                break
        
        if datasource_found == False:
            logging.warning("Unable to find datasource with name: " + datasource_name)
            return

        url = self.client.base_url + "gateways/" + self.gateway_json['id'] + "/datasources/" + self.datasource_json['id']
        
        response = requests.get(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info("Successfully retrieved datasources.")
            self.datasource = response.json()
            return self.datasource
        else:
            logging.error("Failed to retrieve datasources.")
            self.client.force_raise_http_error(response)

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-datasource-status
    def get_datasource_status(self, gateway_name: str, datasource_name: str) -> List:
        self.client.check_token_expiration()
        self.get_datasources(gateway_name)
        datasource_found = False

        for item in self.datasources: 
            if item["datasourceName"] == datasource_name: 
                logging.info("Found datasource with name: " + datasource_name)
                datasource_found = True
                self.datasource_json = item
                break
        
        if datasource_found == False:
            logging.warning("Unable to find datasource with name: " + datasource_name)
            return

        url = self.client.base_url + "gateways/" + self.gateway_json['id'] + "/datasources/" + self.datasource_json['id'] + "/status"
        
        response = requests.get(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info("Successfully retrieved datasources.")
            self.datasource_status = response.content
            return self.datasource_status
        else:
            logging.error("Failed to retrieve datasources.")
            self.client.force_raise_http_error(response)

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/create-datasource
    def create_datasource(self, gateway_name: str, datasource_name: str) -> str:
        self.client.check_token_expiration()
        self.get_gateway(gateway_name)
        self.payload_string_builder('Basic')

        url = self.client.base_url + "gateways/" + self.gateway['id'] + "/datasources"

        payload = {
            "dataSourceType": "Sql",
            "connectionDetails": self.connection_details,
            "datasourceName": datasource_name,
            "credentialDetails": {
                "credentialType": "Basic",
                "credentials": self.encrypted_credentials,
                "encryptedConnection": "Encrypted",
                "encryptionAlgorithm": "RSA-OAEP",
                "privacyLevel": "Organizational",
                "useCallerAADIdentity": "False",
                "useEndUserOAuth2Credentials": "False"
            }
        }

        response = requests.post(url, json = payload, headers = self.client.json_headers)

        if response.status_code == self.client.http_created_code:
            logging.info("Successfully created datasource with name: " + datasource_name)
            self.dataset_parameters = response.content
            return self.dataset_parameters
        else:
            logging.error("Failed to create datasource with name: " + datasource_name)
            self.client.force_raise_http_error(response)

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/update-datasource
    def update_datasource(self, gateway_name: str, datasource_name: str) -> str:
        self.client.check_token_expiration()
        self.get_datasource(gateway_name, datasource_name)
        self.get_gateway(gateway_name)
        self.payload_string_builder('Basic')

        url = self.client.base_url + "gateways/" + self.gateway_json['id'] + "/datasources/" + self.datasource_json['id']

        payload = {
            "credentialDetails": {
                "credentialType": "Basic",
                "credentials": self.encrypted_credentials,
                "encryptedConnection": "Encrypted",
                "encryptionAlgorithm": "RSA-OAEP",
                "privacyLevel": "Organizational",
                "useCallerAADIdentity": "False",
                "useEndUserOAuth2Credentials": "True"
            }
        }
                
        response = requests.patch(url, json = payload, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info("Successfully updated datasource with name: " + datasource_name + " and id: ")
            self.dataset_parameters = response.content
            return self.dataset_parameters
        else:
            logging.error("Failed to retrieve workspaces.")
            self.client.force_raise_http_error(response)

    # https://learn.microsoft.com/en-us/rest/api/power-bi/gateways/get-datasource-users
    def get_datasource_users(self, gateway_name: str, datasource_name: str) -> List:
        self.client.check_token_expiration()
        self.get_datasources(gateway_name)
        datasource_found = False

        for item in self.datasources: 
            if item["datasourceName"] == datasource_name: 
                logging.info("Found datasource with name: " + datasource_name)
                datasource_found = True
                self.datasource_json = item
                break
        
        if datasource_found == False:
            logging.warning("Unable to find datasource with name: " + datasource_name)
            return

        url = self.client.base_url + "gateways/" + self.gateway_json['id'] + "/datasources/" + self.datasource_json['id'] + "/users"
        
        response = requests.get(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info("Successfully retrieved datasources users.")
            self.datasources_users = response.json()["value"]
            return self.datasources_users
        else:
            logging.error("Failed to retrieve datasources users.")
            self.client.force_raise_http_error(response)
    
    # https://learn.microsoft.com/en-us/rest/api/power-bi/gateways/delete-datasource
    def delete_gateway_datasource(self, gateway_name: str, datasource_name: str) -> str:
        self.client.check_token_expiration()
        self.get_datasources(gateway_name)
        datasource_found = False

        for item in self.datasources: 
            if item["datasourceName"] == datasource_name: 
                logging.info("Found datasource with name: " + datasource_name)
                datasource_found = True
                self.datasource_json = item
                break
        
        if datasource_found == False:
            logging.warning("Unable to find datasource with name: " + datasource_name)
            return

        url = self.client.base_url + "gateways/" + self.gateway_json['id'] + "/datasources/" + self.datasource_json['id'] 
        
        response = requests.delete(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            self.datasource = None
            return logging.info("Successfully deleted datasource: " + datasource_name + " in gateway: " + gateway_name)
        else:
            logging.error("Failed to delete datasource: " + datasource_name + " in gateway: " + gateway_name)
            self.client.force_raise_http_error(response)

    # https://learn.microsoft.com/en-us/rest/api/power-bi/gateways/delete-datasource-user
    def delete_gateway_datasource_user(self, gateway_name: str, datasource_name: str, email_address: str) -> str:
        self.client.check_token_expiration()
        self.get_datasource_users(gateway_name, datasource_name)
        user_found = False

        for item in self.datasources_users: 
            if item["emailAddress"] == email_address: 
                logging.info("Found email address " + email_address + "in datasource " + datasource_name + "." )
                user_found = True
                self.user_json = item
                break
        
        if user_found == False:
            logging.warning("Unable to find email address " + email_address + "in datasource " + datasource_name + ".")
            return

        url = self.client.base_url + "gateways/" + self.gateway_json['id'] + "/datasources/" + self.datasource_json['id']  + "/users/" + self.user_json['identifier']
        
        response = requests.delete(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            self.datasource = None
            return logging.info("Successfully deleted user: " + email_address + " from datasource: " + datasource_name + " in gateway: " + gateway_name)
        else:
            logging.error("Failed to delete user: " + email_address + " from datasource: " + datasource_name + " in gateway: " + gateway_name)
            self.client.force_raise_http_error(response)
    
    # https://learn.microsoft.com/en-us/rest/api/power-bi/gateways/add-datasource-user
    def add_gateway_datasource_user(self, gateway_name: str, datasource_name: str, user_name: str, access_type: str, principal_type: str) -> str:
        self.client.check_token_expiration()
        self.get_datasources(gateway_name)
        datasource_found = False

        for item in self.datasources: 
            if item["datasourceName"] == datasource_name: 
                logging.info("Found datasource with name: " + datasource_name)
                datasource_found = True
                self.datasource_json = item
                break
        
        if datasource_found == False:
            logging.warning("Unable to find datasource with name: " + datasource_name)
            return

        url = self.client.base_url + "gateways/" + self.gateway_json['id'] + "/datasources/" + self.datasource_json['id']  + "/users"
        
        error_parameter = ''
        
        if principal_type not in ['App', 'Group', 'None', 'User']:
            error_parameter = 'principal type'
        elif access_type not in ['None', 'Read', 'ReadOverrideEffectiveIdentity']:
            error_parameter = 'access type'
        if error_parameter != '':
            logging.error(f'Issue with adding permission for {user_name} due to incorrect {error_parameter} to datasource {datasource_name} on gateway {gateway_name}.')
            return None
        if principal_type in ['App', 'Group']:
            payload = {
                    "identifier": user_name, 
                    "principalType": principal_type,
                    "datasourceAccessRight": access_type
                }
        elif principal_type in ['User']:
            payload = {
                    "emailAddress": user_name, 
                    "datasourceAccessRight": access_type
                }

        response = requests.post(url, json = payload, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info(f"Successfully adding user {user_name} with access {access_type} as {principal_type} to datasource {datasource_name} on gateway {gateway_name}.")
            self.dataset_permission_updated = True
            return self.dataset_permission_updated
        else:
            logging.error(f"Failed to add user {user_name} to datasource {datasource_name} on gateway {gateway_name}.")
            self.client.force_raise_http_error(response)