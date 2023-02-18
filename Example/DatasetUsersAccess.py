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
from pbi_rest_client.users import Users

logging.basicConfig(level=logging.ERROR )

client = RestClient()
workspaces = Workspaces(client)
datasets = Datasets(client)
users = Users(client)

workspace_name = ''
dataset_name = ''

#################################################################################
# refresh user access
#################################################################################

# users.refresh_user_access(True)

#################################################################################
# Checks users in datasets
#################################################################################
all_datasets = datasets.get_datasets_in_workspace(workspace_name)

for dataset in all_datasets:
    if dataset['name'] == dataset_name:
        users = datasets.get_dataset_users(workspace_name, dataset_name)
        print('        users for dataset',dataset['name'], ':')
        for user in users:
            print('             ',user)


#################################################################################
# Change all dataset ownership to current scrip user
#################################################################################
current_user = 'emailaddress@example.com'
groups= workspaces.get_workspaces()
dataset_list = []
name_list = []
workspace_found = False
for workspace in groups:
    HasUsageMetricsReport = False
    workspace_name = workspace['name']
    all_datasets = datasets.get_datasets_in_workspace(workspace_name)
    for dataset in all_datasets:
        dataset_name = dataset['name']
        name_list.append(f'{dataset_name} in {workspace_name}')

        if dataset['configuredBy'].lower() != current_user:
            for i in range(1,5):
                time.sleep(2)
                datasets.take_dataset_owner(dataset_name, workspace_name)
                dataset_check = datasets.get_dataset_in_workspace(workspace_name, dataset_name)
                # print(dataset_check)
                if dataset_check['configuredBy'].lower() == current_user:
                    print(f'Succefull ownership taken over for {dataset_name} in {workspace_name}.')
                    break
                print(f'Unsuccefull ownership taken over number {i} for {dataset_name} in {workspace_name}.')
                if i == 5:
                    print(f'            Attempt aborted for ownership taken for {dataset_name} in workspace {workspace_name}.')

for name in name_list:
    print(name)