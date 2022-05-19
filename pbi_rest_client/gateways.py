#!/usr/bin/env python

import logging
import requests
import os

from typing import List
from string import Template
from .rest_client import RestClient
from .helpers.serializecredentials import Helpers
from .helpers.asymmetrickeyencryptor import AsymmetricKeyEncryptor

class Gateways:
    def __init__(self, authz_header = None, token = None, token_expiration = None):
        self.client = RestClient(authz_header, token, token_expiration)
        self.helpers = Helpers()
        self._gateway = {}
        self._gateway_parameters = {}
        self._gateway_json = {}
        self._gateways = None
        self._datasource = None
        self._datasources = {}
        self._datasource_json = {}
        self._server_name = None
        self._database_name = None
        self._connection_details = None
        self._credential_details = None
        self._encrypted_credentials = None

    def payload_string_builder(self, credential_type: str) -> str:
        self._server_name = os.getenv('AZURE_SERVER_NAME')
        self._database_name = os.getenv('AZURE_DB_NAME')
        datasource_username = os.getenv('DATASOURCE_USERNAME')
        datasource_password = os.getenv('DATASOURCE_PASSWORD')
        credential_array = [datasource_username, datasource_password]

        connection_details = Template("{\"server\":\"$server_name\",\"database\":\"$database_name\"}")
        self._connection_details = connection_details.substitute(server_name=self._server_name, database_name=self._database_name)
        
        credential_details = self.helpers.serialize_credentials(credential_array, credential_type)

        public_key = {
            'exponent': self._gateway['publicKey']['exponent'],
            'modulus': self._gateway['publicKey']['modulus']
        }

        key_encryptor = AsymmetricKeyEncryptor(public_key)
        self._encrypted_credentials = key_encryptor.encode_credentials(credential_details)

        return self._connection_details, self._encrypted_credentials

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-gateways
    def get_gateways(self) -> List:
        self.client.check_token_expiration()

        url = self.client.base_url + "gateways"
        
        response = requests.get(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info("Successfully retrieved gateways.")
            self._gateways = response.json()["value"]
            return self._gateways
        else:
            logging.error("Failed to retrieve gateways.")
            self.client.force_raise_http_error(response)

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-gateway
    def get_gateway(self, gateway_name: str) -> List:
        self.client.check_token_expiration()
        self.get_gateways()
        gateway_found = False

        for item in self._gateways: 
            if item["name"] == gateway_name: 
                logging.info("Found gateway with name " + gateway_name)
                gateway_found = True
                self._gateway_json = item
                break

        if gateway_found == False:
            logging.warning("Unable to find gateway with name: " + gateway_name)
            return

        url = self.client.base_url + "gateways/" + self._gateway_json['id']
        
        response = requests.get(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info("Successfully retrieved gateway with name: " + gateway_name)
            self._gateway = response.json()
            return self._gateway
        else:
            logging.error("Failed to retrieve gateway with name: " + gateway_name)
            self.client.force_raise_http_error(response)

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-datasources
    def get_datasources(self, gateway_name: str) -> List:
        self.client.check_token_expiration()
        self.get_gateway(gateway_name)

        url = self.client.base_url + "gateways/" + self._gateway['id'] + "/datasources"
        
        response = requests.get(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info("Successfully retrieved datasources.")
            self._datasources = response.json()["value"]
            return self._datasources
        else:
            logging.error("Failed to retrieve datasources.")
            self.client.force_raise_http_error(response)

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-datasource
    def get_datasource(self, gateway_name: str, datasource_name: str) -> List:
        self.client.check_token_expiration()
        self.get_datasources(gateway_name)
        datasource_found = False

        for item in self._datasources: 
            if item["datasourceName"] == datasource_name: 
                logging.info("Found datasource with name: " + datasource_name)
                datasource_found = True
                self._datasource_json = item
                break
        
        if datasource_found == False:
            logging.warning("Unable to find datasource with name: " + datasource_name)
            return

        url = self.client.base_url + "gateways/" + self._gateway_json['id'] + "/datasources/" + self._datasource_json['id']
        
        response = requests.get(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info("Successfully retrieved datasources.")
            self._datasource = response.json()
            return self._datasource
        else:
            logging.error("Failed to retrieve datasources.")
            self.client.force_raise_http_error(response)

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-datasource-status
    def get_datasource_status(self, gateway_name: str, datasource_name: str) -> List:
        self.client.check_token_expiration()
        self.get_datasources(gateway_name)
        datasource_found = False

        for item in self._datasources: 
            if item["datasourceName"] == datasource_name: 
                logging.info("Found datasource with name: " + datasource_name)
                datasource_found = True
                self._datasource_json = item
                break
        
        if datasource_found == False:
            logging.warning("Unable to find datasource with name: " + datasource_name)
            return

        url = self.client.base_url + "gateways/" + self._gateway_json['id'] + "/datasources/" + self._datasource_json['id'] + "/status"
        
        response = requests.get(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            logging.info("Successfully retrieved datasources.")
            self._datasource_status = response.content
            return self._datasource_status
        else:
            logging.error("Failed to retrieve datasources.")
            self.client.force_raise_http_error(response)

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/create-datasource
    def create_datasource(self, gateway_name: str, datasource_name: str) -> str:
        self.client.check_token_expiration()
        self.get_gateway(gateway_name)
        self.payload_string_builder('Basic')

        url = self.client.base_url + "gateways/" + self._gateway['id'] + "/datasources"

        payload = {
            "dataSourceType": "Sql",
            "connectionDetails": self._connection_details,
            "datasourceName": datasource_name,
            "credentialDetails": {
                "credentialType": "Basic",
                "credentials": self._encrypted_credentials,
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
            self._dataset_parameters = response.content
            return self._dataset_parameters
        else:
            logging.error("Failed to create datasource with name: " + datasource_name)
            self.client.force_raise_http_error(response)

    # https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/update-datasource
    def update_datasource(self, gateway_name: str, datasource_name: str) -> str:
        self.client.check_token_expiration()
        self.get_datasource(gateway_name, datasource_name)
        self.get_gateway(gateway_name)
        self.payload_string_builder('Basic')

        url = self.client.base_url + "gateways/" + self._gateway_json['id'] + "/datasources/" + self._datasource_json['id']

        payload = {
            "credentialDetails": {
                "credentialType": "Basic",
                "credentials": self._encrypted_credentials,
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
            self._dataset_parameters = response.content
            return self._dataset_parameters
        else:
            logging.error("Failed to retrieve workspaces.")
            self.client.force_raise_http_error(response)