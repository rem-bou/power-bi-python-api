#!/usr/bin/env python

import logging, time

#################################################################################
# Only usefull as this script is within sub-directory of the project
# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
#################################################################################
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
#################################################################################

from pbi_rest_client.rest_client import RestClient
from pbi_rest_client.workspaces import Workspaces
from pbi_rest_client.datasets import Datasets
from pbi_rest_client.gateways import Gateways
from pbi_rest_client.reports import Reports

logging.basicConfig(level=logging.ERROR)

client = RestClient()
workspaces = Workspaces(client)
datasets = Datasets(client)
gateways = Gateways(client)
reports = Reports(client)

gateway_name = ''
workspace_name = ''
dataset_name = ''

#################################################################################
# Takes Ownership and bind data to datasource from getway
#################################################################################
datasets_list = datasets.get_datasets_in_workspace(workspace_name)

for dataset in datasets_list:
    if dataset['name'] == dataset_name:
        datasets.take_dataset_owner(dataset_name, workspace_name)
        time.sleep(10)
        datasources = datasets.get_datasources(dataset_name,workspace_name)
        for datasource in datasources:
            print(datasource)

        binding_result = datasets.bind_to_gateway(workspace_name,dataset_name)
        if binding_result==True:
            gateway_list = datasets.get_dataset_gateways(dataset_name,workspace_name)
            print(gateway_list)
            time.sleep(10)
            
            datasources = datasets.get_datasources(dataset_name,workspace_name)
            for datasource in datasources:
                print(datasource)
            datasets.refresh_dataset(dataset_name, workspace_name)

#################################################################################
# Clone Report and rebind it to different dataset
#################################################################################

# reports.clone_report(workspace_name='', report_name='', clone_report_name='', target_dataset_name='')
# reports.rebind_report(workspace_name='', report_name='', target_dataset_name='')