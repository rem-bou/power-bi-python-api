#!/usr/bin/env python
import datetime
from datetime import datetime, timezone
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
from pbi_rest_client.reports import Reports

logging.basicConfig(level=logging.INFO)

client = RestClient()
workspaces = Workspaces(client)
datasets = Datasets(client)
reports = Reports(client)


#################################################################################
# Refresh dataset and checks Top X Refresh
#################################################################################

def refresh_print(refreshes, show_error: bool = False):
    ######################################################
    # Refresh Details - formating output function
    ######################################################
    for refresh in refreshes:
        # print(refresh)
        if refresh['status'] != 'Unknown':
            c = datetime.strptime(refresh['endTime'][:19], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(refresh['startTime'][:19], '%Y-%m-%dT%H:%M:%S')
        
            refresh_update = refresh
            refresh_update['refreshLength'] = str(c)
            refresh_update['endTime'] =  datetime.strftime(datetime.strptime(refresh_update['endTime'][:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc).astimezone(tz=None), '%Y-%m-%d %H:%M:%S')
            refresh_update['startTime'] = datetime.strftime(datetime.strptime(refresh_update['startTime'][:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc).astimezone(tz=None), '%Y-%m-%d %H:%M:%S')
            
        else:
            refresh_update = refresh
            c = datetime.strptime(datetime.strftime(datetime.now(timezone.utc), '%Y-%m-%dT%H:%M:%S'), '%Y-%m-%dT%H:%M:%S') - datetime.strptime(refresh['startTime'][:19], '%Y-%m-%dT%H:%M:%S')
            refresh_update['refreshLength'] = str(c)
            refresh_update['startTime'] = datetime.strftime(datetime.strptime(refresh_update['startTime'][:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc).astimezone(tz=None), '%Y-%m-%d %H:%M:%S')
        
        if show_error and refresh['status'] == 'Failed' and refresh['refreshType'] == 'ViaEnhancedApi':
            refresh_detail = datasets.get_dataset_refresh_details(dataset_name, workspace_name, refresh['requestId'])
            refresh_update['refresh_detail'] = refresh_detail['messages'][0]
        
        print('             ',refresh_update)
        if show_error and refresh['status'] == 'Failed'and refresh['refreshType'] == 'ViaEnhancedApi': 
            print('             ', refresh_update['refresh_detail'])


workspace_name = ''
dataset_name = ''


######################################################
# cancel or start dataset refresh 
######################################################

# datasets.cancel_dataset_refresh(dataset_name,workspace_name)

# datasets.refresh_dataset(dataset_name, workspace_name, 'Full')



######################################################
# Dataset Details
######################################################

# data = datasets.get_dataset_in_workspace(workspace_name = workspace_name, dataset_name =  dataset_name)
# print(data)

######################################################
# Dataset Refresh History
######################################################

refresh_status = 'Unknown'
first_run = 1
retest = True
timer_length = 30
while refresh_status == 'Unknown':
    if first_run == 1:
        refreshes = datasets.get_dataset_refresh_history(workspace_name, dataset_name, 5)
        first_run = first_run + 1
    else:
        refreshes = datasets.get_dataset_refresh_history(workspace_name, dataset_name, 1)
    refresh_print(refreshes, show_error = False)
    if retest != True: break
    refresh_status = refreshes[0]['status']
    if refresh_status == 'Unknown': 
        print(f'Waiting {timer_length}s before new check')
        time.sleep(timer_length)
